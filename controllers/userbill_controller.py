from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session 
from models import BillUser
from services.authservice import AuthService

router = APIRouter(prefix="/userbill", tags=["UserBill"])
auth_service = AuthService()

@router.get("/bills/{userid}")
def get_user_bills(
    userid: str,  # Add this parameter to capture the path variable
    session: Session = Depends(get_session),
    token: str = Depends(auth_service.oauth2_scheme)
):
    # 1. Decode the token to get the user data
    payload = auth_service.decode_access_token(token)
    
    # 2. Safety Check: If token is invalid or expired
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Get the user ID from the "sub" (subject) claim
    authenticated_user_id = payload.get("sub")
    
    # 4. Security Check: Verify the authenticated user is requesting their own bills
    # (Optional but recommended for security)
    if authenticated_user_id != userid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own bills"
        )
    
    # 5. Query all bills for this user
    statement = select(BillUser).where(BillUser.user_id == userid)
    bills = session.exec(statement).all()
    
    # 6. Calculate total receivable and payable
    total_receivable = sum(bill.amount for bill in bills if bill.type == "receivable")
    
    return {
        "value": total_receivable,
    }