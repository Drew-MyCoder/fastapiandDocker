from sqlalchemy import Table, Column, Integer, String, DateTime, Sequence, MetaData

metadata = MetaData()

users = Table(
    "py_users", metadata,
    Column("id", Integer, Sequence("user_id_seq"), primary_key=True),
    Column("email", String(100)),
    Column("password", String(100)),
    Column("fullname", String(50)),
    Column("created_on", DateTime),
    Column("status", String(1))
)

codes = Table(
    "py_codes", metadata,
    Column("id", Integer, Sequence("code_id_seq"), primary_key=True),
    Column("email", String(100)),
    Column("reset_code", String(50)),
    Column("status", String(1)),
    Column("expired_in", DateTime)
)


blacklists = Table(
    "py_blacklists", metadata,
    Column("token", String(250), unique=True),
    Column("email", String(100)),
)


otps = Table(
    "py_otps", metadata,
    Column("id", Integer, Sequence("otp_id_seq"), primary_key=True),
    Column("recipient_id", String(100)),
    Column("session_id", String(100)),
    Column("otp_code", String(6)),
    Column("status", String(1)),
    Column("created_on", DateTime),
    Column("updated_on", DateTime),
    Column("otp_failed_count", Integer, default=0)
)


otpBlocks = Table(
    "py_otp_blocks", metadata,
    Column("id", Integer, Sequence("otp_block_id_seq"), primary_key=True),
    Column("recipient_id", String(100)),
    Column("created_on", DateTime),
)