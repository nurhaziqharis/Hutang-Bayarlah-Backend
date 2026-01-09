from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginResponse(BaseModel):
    issuccess: bool
    access_token: Optional[str] = None
    token_type: Optional[str] = None