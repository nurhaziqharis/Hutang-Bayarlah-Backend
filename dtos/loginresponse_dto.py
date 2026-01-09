from pydantic import BaseModel, EmailStr
from typing import Optional
from dtos.user_dto import UserDTO

class LoginResponse(BaseModel):
    issuccess: bool
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    user: Optional[UserDTO] = None