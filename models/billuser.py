from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel

class BillUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_email: str
    bill_title: str
    bill_date: datetime
    value: Decimal
    
    # Relationships
    user_id: int = Field(foreign_key="user.id")
    bill_id: int = Field(foreign_key="bill.id")