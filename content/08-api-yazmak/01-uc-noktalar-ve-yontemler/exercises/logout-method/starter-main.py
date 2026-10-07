from fastapi import FastAPI

app = FastAPI()
session = {"logged_in": True}


@app.get("/logout")
def logout():
    session["logged_in"] = False
    return session
