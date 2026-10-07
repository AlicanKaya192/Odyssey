from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/authors", tags=["authors"])
authors = {1: "Frank Herbert", 2: "Jane Austen"}


@router.get("")
def list_authors():
    return authors


@router.get("/{author_id}")
def read_author(author_id: int):
    if author_id not in authors:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"id": author_id, "name": authors[author_id]}
