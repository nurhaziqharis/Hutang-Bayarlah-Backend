from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session 
from models import User
from dtos.createuserrequest_dto import CreateUserRequest
from dtos.createuserresponse_dto import CreateUserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=CreateUserResponse)
def create_user(
    user: CreateUserRequest,
    session: Session = Depends(get_session)
):
    # 1️⃣ Check existing user
    existing_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with this email already exists"
    )

    # 2️⃣ Create user
    user_to_create = User(
        fullname=user.fullname,
        email=user.email,
        password=user.password,
        role=user.role
    )

    # 3️⃣ Save
    session.add(user_to_create)
    session.commit()
    session.refresh(user_to_create)

    # 4️⃣ Response
    return CreateUserResponse(
        fullname=user_to_create.fullname,
        email=user_to_create.email,
        role=user_to_create.role,
        message="User created successfully"
    )


@router.get("/")
def get_all_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()