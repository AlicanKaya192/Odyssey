from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
contacts = {}
next_id = 1

# Address book: ContactIn (name at least 1, phone at least 3 chars), ContactPatch, ContactOut (+ id)
# POST /contacts (201), GET /contacts, GET /contacts/{id},
# PATCH /contacts/{id}, DELETE /contacts/{id} (204); 404 "Contact not found" if missing
