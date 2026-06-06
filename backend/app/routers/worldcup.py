from fastapi import APIRouter, Depends
from ..database import get_categories
from ..auth import get_current_user
from ..models import WorldCupCategory

router = APIRouter(prefix="/api/worldcup", tags=["worldcup"])

@router.get("/categories", response_model=list[WorldCupCategory])
def list_categories(_=Depends(get_current_user)):
    return get_categories()
