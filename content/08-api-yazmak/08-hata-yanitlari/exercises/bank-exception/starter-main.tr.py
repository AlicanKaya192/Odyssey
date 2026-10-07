from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
accounts = {"ada": 100, "alan": 20}

# InsufficientFunds(Exception): balance alani olan istisna
# withdraw(name, amount): bakiye yetmezse InsufficientFunds(bakiye) firlat, yoksa dus ve yeni bakiyeyi dondur
# Yakalayici: 400, {"error": "insufficient_funds", "balance": ...}
# POST /accounts/{name}/withdraw?amount=.. -> {"name", "balance"}
