from email.policy import default
from enum import unique
from sqlalchemy.types import Boolean
from sqlalchemy import Column, Integer, String, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UsersOperations(Base):
    __tablename__ = "users_operations"

    id = Column(Integer, primary_key=True)
    bot_user_id = Column(BigInteger, nullable=False)
    bill_id = Column(String(64))
    paid = Column(Boolean)
    bill_amount = Column(Float)
    admin_ch = Column(Float)


class BlockUsers(Base):
    __tablename__ = "block_users"

    id = Column(Integer, primary_key=True)
    bot_user_id = Column(BigInteger, nullable=False)
