from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
contacts = {}
next_id = 1

# Rehber: ContactIn (name en az 1, phone en az 3 karakter), ContactPatch, ContactOut (+ id)
# POST /contacts (201), GET /contacts, GET /contacts/{id},
# PATCH /contacts/{id}, DELETE /contacts/{id} (204); bulunamazsa 404 "Contact not found"
