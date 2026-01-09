from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUserRequest(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    role: str = "user"