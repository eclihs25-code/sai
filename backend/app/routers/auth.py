from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_user, verify_password
from ..auth import create_access_token, get_current_user
from ..models import Token, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )
    token = create_access_token({"sub": user.username})
    return Token(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    return UserOut(id=current.id, username=current.username, role=current.role)
