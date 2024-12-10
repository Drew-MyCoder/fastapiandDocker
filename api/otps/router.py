from fastapi import APIRouter, HTTPException, status
from . import schema, crud
from api.enums import otp
from api.utils import otpUtil, emailUtil
import uuid

router = APIRouter(prefix="/api/v1")


@router.post("/otp/send")
async def send_otp(
    type: otp.OTPType,
    request: schema.CreateOTP
):
    # check block otp
    otp_blocks = await crud.find_block_otp(request.recipient_id)
    if otp_blocks:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Sorry, this phone number is blocked. try in 5 minutes")
    
    # generate and save to table py_otps
    otp_code = otpUtil.random(6)
    session_id = str(uuid.uuid1())
    await crud.save_otp(request, session_id, otp_code)

    # Send OTP to email
    if type == otp.OTPType.email:
        # Sending email
        subject = "OTP Code"
        recipient = [request.recipient_id]
        message = """
            <!DOCTYPE html>
            <html>
            <title>Reset Password</title>
            <body>
            <div style="width:100%;font-family: monospace;">
                <h1>{0:}</h1>
            </div>
            </body>
            </html>
            """.format(otp_code)

        await emailUtil.send_email(subject, recipient, message)

    else:
        print("OTP via phone number")

    return {
        "session_id": session_id,
        "otp_code": otp_code,
    }


@router.post("/otp/verify")
async def verify_otp(request: schema.VerifyOTP):
    # check block otp
    otp_blocks = await crud.find_block_otp(request.recipient_id)
    if otp_blocks:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Sorry, this phone number is blocked. try in 5 minutes")
    
    # check otp code 6 digit lifetime (expires in 60 secs)
    otp_result = await crud.find_otp_lifetime(request.recipient_id, request.session_id)
    if not otp_result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="OTP has expired, request a new one pls")

    otp_result = schema.OTPList(**otp_result)

    # check if otp code is already used
    if otp_result == "9":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="OTP has been used, request a new one pls")

    # verify otp code,
    # if not verified,
    if otp_result.otp_code != request.otp_code:
        await crud.update_otp_failed_count(otp_result)

        # if otp failed count 5 times, then block otp (py_otp_blocks)
        if otp_result.otp_failed_count + 1 == 5:
            await crud.save_block_otp(otp_result)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail="Sorry, this phone number is blocked. try in 5 minutes")
    

        # throw exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="the otp code you've entered is incorrect")

    # disable otp code if successfully verified
    await crud.disable_otp_code(otp_result)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "OTP verified successfully"
    }