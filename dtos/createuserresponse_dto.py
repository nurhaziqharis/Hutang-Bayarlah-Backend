from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUserResponse(BaseModel):
    fullname: str
    email: EmailStr
    role: str = "user"
    message: str