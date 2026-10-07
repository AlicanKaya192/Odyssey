from fastapi import BackgroundTasks, FastAPI

app = FastAPI()
outbox = []


def send_welcome(email: str):
    outbox.append(f"Welcome, {email}!")


# POST /signup?email=.. -> send_welcome'u arka plan isi olarak ekle, hemen {"queued": true} don
# GET /outbox -> outbox listesi
