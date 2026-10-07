from fastapi import BackgroundTasks, FastAPI

app = FastAPI()
outbox = []


def send_welcome(email: str):
    outbox.append(f"Welcome, {email}!")


@app.post("/signup")
def signup(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_welcome, email)
    return {"queued": True}


@app.get("/outbox")
def show_outbox():
    return outbox
