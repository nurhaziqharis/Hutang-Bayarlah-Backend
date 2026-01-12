from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
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
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    # Default to 30 minutes if not in .env
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # 1. Password Hashing (Using direct bcrypt for Python 3.14 compatibility)
    def get_password_hash(self, password: str):
        # Truncate to 72 bytes for bcrypt compatibility
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str):
        try:
            password_bytes = plain_password.encode('utf-8')[:72]
            return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
        except Exception:
            return False

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
            return None 
        except jwt.InvalidTokenError:
            return None 

    # --- Handlers ---

    def register_handler(self, email: str, password: str, get_user_by_email, create_user):
        """ Handles the registration logic """
        existing_user = get_user_by_email(email)
        if existing_user:
            return None 

        hashed_password = self.get_password_hash(password)
        new_user = create_user(email=email, password=hashed_password)
        return new_user 
        
    def login_handler(self, email: str, password: str, get_user_by_email):
    # 1. Fetch user
        user = get_user_by_email(email)
        if not user:
            return None
        
        # 2. Verify password
        if not self.verify_password(password, user.password):
            return None
        
        # 3. Create JWT
        access_token = self.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        # 4. Return the dictionary that matches LoginResponse DTO exactly
        return {
            "issuccess": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": getattr(user, 'name', None)
            }
        }
    
    def check_user_authorization(self, jwttoken: str, userid: str) -> bool:
        payload = self.decode_access_token(jwttoken)
    
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
        authenticated_user_id = payload.get("sub")
        if str(authenticated_user_id) != str(userid):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own bills"
            )
    
        return True
