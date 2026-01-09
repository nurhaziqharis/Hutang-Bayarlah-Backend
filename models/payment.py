from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from sqlmodel import Field, SQLModel, Relationship

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Attributes
    value: Decimal
    payment_date: datetime = Field(default_factory=datetime.utcnow)
    payment_status: str # e.g., "pending", "completed"

    # Foreign Keys
    user_id: int = Field(foreign_key="user.id")
    bill_user_id: int = Field(foreign_key="billuser.id")