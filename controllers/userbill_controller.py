from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session 
from models import BillUser
from services.authservice import AuthService
from services.billservice import BillService
from dtos.newbill_dto import NewBillDTO

router = APIRouter(prefix="/userbill", tags=["UserBill"])
auth_service = AuthService()

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

@router.post("/bill")
async def save_new_bill(
    bill_data: NewBillDTO,
    session: Session = Depends(get_session),
    token: str = Depends(auth_service.oauth2_scheme)
):
    current_user = auth_service.get_current_user(token)
    userid = current_user.id 

    try:
        # new_record = BillService.create_new_bill(userid, bill_data, session)
        print(bill_data)
        
        return {
            "status": "success",
            "message": "Bill saved successfully",
            "data": new_record
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not save bill: {str(e)}"
        )