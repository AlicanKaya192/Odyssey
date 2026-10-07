from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
accounts = {"ada": 100, "alan": 20}


class InsufficientFunds(Exception):
    def __init__(self, balance: int):
        self.balance = balance


def withdraw(name: str, amount: int) -> int:
    if accounts[name] < amount:
        raise InsufficientFunds(accounts[name])
    accounts[name] -= amount
    return accounts[name]


@app.exception_handler(InsufficientFunds)
def funds_handler(request: Request, exc: InsufficientFunds):
    return JSONResponse(status_code=400,
                        content={"error": "insufficient_funds", "balance": exc.balance})


@app.post("/accounts/{name}/withdraw")
def withdraw_money(name: str, amount: int):
    return {"name": name, "balance": withdraw(name, amount)}
