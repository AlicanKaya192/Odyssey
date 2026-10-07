from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
contacts = {}
next_id = 1


class ContactIn(BaseModel):
    name: str = Field(min_length=1)
    phone: str = Field(min_length=3)


class ContactPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    phone: str | None = Field(default=None, min_length=3)


class ContactOut(ContactIn):
    id: int


def find_contact(contact_id: int) -> dict:
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts[contact_id]


@app.post("/contacts", status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactIn) -> ContactOut:
    global next_id
    record = {"id": next_id, **contact.model_dump()}
    contacts[next_id] = record
    next_id += 1
    return record


@app.get("/contacts")
def list_contacts() -> list[ContactOut]:
    return list(contacts.values())


@app.get("/contacts/{contact_id}")
def read_contact(contact_id: int) -> ContactOut:
    return find_contact(contact_id)


@app.patch("/contacts/{contact_id}")
def update_contact(contact_id: int, patch: ContactPatch) -> ContactOut:
    record = find_contact(contact_id)
    record.update(patch.model_dump(exclude_unset=True))
    return record


@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int):
    find_contact(contact_id)
    del contacts[contact_id]
