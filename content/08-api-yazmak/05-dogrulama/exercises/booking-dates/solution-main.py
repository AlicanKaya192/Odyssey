from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

app = FastAPI()


class Booking(BaseModel):
    check_in: int = Field(ge=1, le=365)
    check_out: int = Field(ge=1, le=365)
    guests: int = Field(default=1, ge=1, le=4)

    @model_validator(mode="after")
    def check_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self


@app.post("/bookings")
def book(booking: Booking):
    return {"nights": booking.check_out - booking.check_in, "guests": booking.guests}
