from fastapi import BackgroundTasks, FastAPI

app = FastAPI()
outbox = []


def send_welcome(email: str):
    outbox.append(f"Welcome, {email}!")


# POST /signup?email=.. -> add send_welcome as a background task, answer {"queued": true} right away
# GET /outbox -> the outbox list
