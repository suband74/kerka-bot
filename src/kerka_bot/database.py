from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, sessionmaker

from settings import POSTGRES_DATABASE_URL
from models import UsersOperations, BlockUsers

engine = create_engine(POSTGRES_DATABASE_URL, echo=True)
session_local = sessionmaker(engine)

def paid(bill_id):
    with session_local() as session:
        it = session.query(UsersOperations).filter_by(bill_id=bill_id).first()
        it.paid = True
        session.add(it)
        session.commit()

def add_bill(user_id, bill_id, amount):
    with session_local() as session:
        
        us = UsersOperations(
            bot_user_id = user_id,
            bill_id = bill_id,
            paid = False,
            bill_amount = amount,           
        )
        session.add(us)
        session.commit()

def user_with_balance():
    with session_local() as session:
        st = session.query(UsersOperations.bot_user_id, func.sum(UsersOperations.bill_amount)).filter_by(paid=True).group_by(UsersOperations.bot_user_id).all()
        return st

def admin_change_balance(id, amount):
     with session_local() as session:
        us = UsersOperations(
            bot_user_id = id,
            paid = True,
            bill_amount = amount,
            admin_ch = amount        
        )
        session.add(us)
        session.commit()

def add_to_db_block_user(user_id):
    with session_local() as session:
        us = BlockUsers(
            bot_user_id = user_id,   
        )
        session.add(us)
        session.commit()

def check_block_user(user_id):
    with session_local() as session:
        if session.query(BlockUsers).filter_by(bot_user_id=user_id).first():
            return True
        return False
