from typing import Optional
from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int
    email: str
    name: Optional[str] = None