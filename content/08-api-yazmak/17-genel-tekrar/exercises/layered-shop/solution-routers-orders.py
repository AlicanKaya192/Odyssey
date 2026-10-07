from fastapi import APIRouter, Depends

from deps import require_key
from errors import OutOfStock
from stock import stock

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(require_key)])


@router.post("/{item}")
def order(item: str):
    if stock.get(item, 0) == 0:
        raise OutOfStock(item)
    stock[item] -= 1
    return {"item": item, "left": stock[item]}
