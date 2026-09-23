from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import EmailStr

from app.database.database import get_db
from app.database import models

from app.schemas.auth import LoginRequest, LoginResponse

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.execute(
        select(models.User).where(
            models.User.email == login_data.email
        )
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
    "access_token": access_token,
    "token_type": "bearer",
    "role": user.role,
    "user_id": user.id,
    "customer_id": user.customer_id,
    "agent_id": user.agent_id
}


# =========================================================
# CUSTOMER REGISTRATION
# =========================================================

@router.post("/register")
def register_customer(
    name: str,
    email: EmailStr,
    password: str,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Check duplicate USER email
    # -----------------------------------------------------

    existing_user = db.execute(
        select(models.User).where(
            models.User.email == email
        )
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # -----------------------------------------------------
    # Check duplicate CUSTOMER email
    # -----------------------------------------------------

    existing_customer = db.execute(
        select(models.Customer).where(
            models.Customer.email == email
        )
    ).scalar_one_or_none()

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Customer with this email already exists"
        )

    # -----------------------------------------------------
    # Create Customer
    # -----------------------------------------------------

    new_customer = models.Customer(
        name=name,
        email=email
    )

    db.add(new_customer)

    # Get customer ID before creating User
    db.flush()

    # -----------------------------------------------------
    # Create User and link Customer
    # -----------------------------------------------------

    new_user = models.User(
        email=email,
        password_hash=hash_password(password),
        role="customer",
        customer_id=new_customer.id
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_customer)
    db.refresh(new_user)

    return {
        "message": "Customer registered successfully",
        "user_id": new_user.id,
        "customer_id": new_customer.id,
        "name": new_customer.name,
        "email": new_user.email,
        "role": new_user.role
    }