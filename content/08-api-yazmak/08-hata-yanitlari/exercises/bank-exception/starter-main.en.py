from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
accounts = {"ada": 100, "alan": 20}

# InsufficientFunds(Exception): an exception with a balance field
# withdraw(name, amount): raise InsufficientFunds(balance) if it's not enough, otherwise subtract and return the new balance
# Handler: 400, {"error": "insufficient_funds", "balance": ...}
# POST /accounts/{name}/withdraw?amount=.. -> {"name", "balance"}
