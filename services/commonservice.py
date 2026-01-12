import contextlib
from database import get_session 
from models import User
from sqlmodel import Session, select

class CommonService:
    
    @staticmethod
    def get_user_by_email(email: str):
        
        get_session_ctx = contextlib.contextmanager(get_session)
        
        with get_session_ctx() as session:
            existing_user = session.exec(
                select(User).where(User.email == email)
            ).first()
            return existing_user if existing_user else None