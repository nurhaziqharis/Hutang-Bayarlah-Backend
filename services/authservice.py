import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Optional
from dotenv import load_dotenv
import os
import bcrypt

class AuthService:

    # Configuration
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # 1. Password Hashing
    # def get_password_hash(self, password: str):
    #     return self.pwd_context.hash(password[:72])

    def get_password_hash(self, password: str):
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str):
        password_bytes = plain_password.encode('utf-8')[:72]
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))

    # 2. JWT Generation
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    # 3. JWT Verification
    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Token invalid
        

    def register_handler(self, email: str, password: str, get_user_by_email, create_user):
        existing_user = get_user_by_email(email)
        if existing_user:
            return None  # User already exists

        hashed_password = self.get_password_hash(password)
        new_user = create_user(email=email, password=hashed_password)
        return new_user 
        
    def login_handler(self, email: str, password: str, get_user_by_email):
        user = get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user