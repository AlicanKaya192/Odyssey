from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

app = FastAPI()

# Booking modeli (gunler yilin kacinci gunu: 1-365):
#   check_in, check_out: 1-365
#   guests: 1-4, varsayilan 1
#   check_out, check_in'den sonra olmali (model_validator)
# POST /bookings -> {"nights": check_out - check_in, "guests"}
