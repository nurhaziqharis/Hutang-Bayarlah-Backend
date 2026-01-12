import contextlib
from database import get_session 
from models import User, BillUser
from sqlmodel import Session, select

class BillService:

    @staticmethod
    def get_bills_from_user(userid: str):
        get_session_ctx = contextlib.contextmanager(get_session)
        with get_session_ctx() as session:
            user_bills = session.exec(
                select(BillUser).where(BillUser.user_id == userid)
            ).all()
            return user_bills