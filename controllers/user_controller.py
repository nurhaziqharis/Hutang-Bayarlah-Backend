from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session 
from models import User
from dtos.createuserrequest_dto import CreateUserRequest
from dtos.createuserresponse_dto import CreateUserResponse
from dtos.loginresponse_dto import LoginResponse
from dtos.loginrequest_dto import LoginRequest
from services.authservice import AuthService
from services.commonservice import CommonService

router = APIRouter(prefix="/users", tags=["Users"])
auth_service = AuthService()

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

    hashed_password = auth_service.get_password_hash(user.password)

    # 2️⃣ Create user
    user_to_create = User(
        fullname=user.fullname,
        email=user.email,
        password=hashed_password,
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


@router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest):
    print("Someone is logged")

    result = auth_service.login_handler(
        email=login_data.email,
        password=login_data.password,
        get_user_by_email=CommonService.get_user_by_email
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result