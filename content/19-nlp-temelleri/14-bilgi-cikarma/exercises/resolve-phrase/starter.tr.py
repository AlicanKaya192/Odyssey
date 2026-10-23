import re
from datetime import datetime, timedelta


def resolve(phrase, reference):
    return "rejected"

REF = "2026-03-14T01:30:00+03:00"
print(resolve("in 2 days at 9am", REF))
print(resolve("Tomorrow at 12am", REF))
print(resolve("tomorrow at 7", REF))
print(resolve("next friday at 5pm", REF))
