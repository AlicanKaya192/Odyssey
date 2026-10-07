from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def stats():
    return {"books": 2}


@router.post("/reset")
def reset():
    return {"reset": True}
