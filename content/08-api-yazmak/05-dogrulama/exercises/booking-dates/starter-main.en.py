from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

app = FastAPI()

# Booking model (days are the day of the year: 1-365):
#   check_in, check_out: 1-365
#   guests: 1-4, default 1
#   check_out must be after check_in (model_validator)
# POST /bookings -> {"nights": check_out - check_in, "guests"}
