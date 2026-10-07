from fastapi import APIRouter, Depends

from deps import require_key

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_key)])


@router.get("/stats")
def stats():
    return {"books": 2}


@router.post("/reset")
def reset():
    return {"reset": True}
