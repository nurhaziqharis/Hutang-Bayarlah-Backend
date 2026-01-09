from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel

class Bill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bill_title: str
    bill_date: datetime = Field(default_factory=datetime.utcnow)
    total_bill: Decimal
    total_tax: Decimal