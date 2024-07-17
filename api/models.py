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