import contextlib
from database import get_session 
from models import User
from sqlmodel import Session, select

from models.bill import Bill

class BillService:
    
    @staticmethod
    def get_bills_by_user_id(user_id: int):
        
        get_session_ctx = contextlib.contextmanager(get_session)
        
        with get_session_ctx() as session:

            statement = select(Bill).where(Bill.user_id == user_id)
            bills = session.exec(statement).all()
            return bills if bills else []
        
        