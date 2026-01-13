from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from .user_dto import UserDTO

class NewBillDTO(BaseModel):
    billtitle: str
    totalbill: Decimal
    totaltax: Decimal
    user: UserDTO