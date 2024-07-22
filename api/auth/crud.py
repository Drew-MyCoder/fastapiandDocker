from api.utils.dbUtil import database
from . import schema


def find_exist_user(email: str):
    query = "select * from py_users where status='1' and email=:email"
    return database.fetch_one(query, values={"email": email})


def save_user(user: schema.UserCreate):
    query = "INSERT INTO py_users VALUES (nextval('user_id_seq'), :email, :password, :fullname, now() at time zone 'UTC', '1')"
    return database.execute(query, values={"email":user.email, "password":user.password, "fullname":user.fullname})


def create_reset_code(email: str, reset_code: str):
    query = "INSERT INTO py_codes VALUES (nextval('code_id_seq'), :email, :reset_code, '1', now() at time zone 'UTC')"
    return database.execute(query, values={"email": email, "reset_code": reset_code})


def check_reset_password_token(reset_password_token: str):
    query= "SELECT * FROM py_codes WHERE status='1' AND reset_code=:reset_password_token AND expired_in >= now() AT TIME ZONE 'UTC' - INTERVAL '10 minutes'"
    return database.fetch_one(query, values={"reset_password_token": reset_password_token})


def reset_password(new_hashed_password: str, email: str):
    query = "UPDATE py_users SET password=:password WHERE email=:email"
    return database.execute(query, values={"password": new_hashed_password, "email":email})


def disable_reset_code(reset_password_token: str, email: str):
    query = "UPDATE py_codes SET status='9' WHERE status='1' AND reset_code=:reset_code AND email=:email "
    return database.execute(query, values={"reset_code": reset_password_token, "email":email})