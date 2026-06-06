from fastapi import APIRouter, Depends
from ..auth import require_admin
from ..database import _users
from ..models import UserOut

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/users", response_model=list[UserOut])
def list_users(_=Depends(require_admin)):
    return [UserOut(id=u.id, username=u.username, role=u.role) for u in _users]
