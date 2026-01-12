from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session 
from models import BillUser
from services.authservice import AuthService
from services.billservice import BillService

router = APIRouter(prefix="/userbill", tags=["UserBill"])
auth_service = AuthService()

# To get all bills for current user
@router.get("/bills/{userid}")
def get_user_bills(
    userid: str,
    session: Session = Depends(get_session),
    token: str = Depends(auth_service.oauth2_scheme)
):
    auth_service.check_user_authorization(token, userid)
    bill_user = BillService.get_bills_from_user(userid)
    total_receivable = sum(bill.amount for bill in bill_user if bill.type == "receivable")
    
    return {
        "total_receivable": total_receivable,
    }