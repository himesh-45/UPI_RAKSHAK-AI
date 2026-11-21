from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.db_models import User
from ..models.schemas import LoginRequest, TokenResponse
from ..core.auth import verify_password, create_access_token, get_current_admin
from ..core.security import sanitize_text

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    email = sanitize_text(req.email.lower())
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(data={"sub": user.email})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        email=user.email
    )

@router.get("/me")
def get_me(current_admin: User = Depends(get_current_admin)):
    return {
        "id": current_admin.id,
        "email": current_admin.email,
        "created_at": current_admin.created_at.isoformat()
    }
