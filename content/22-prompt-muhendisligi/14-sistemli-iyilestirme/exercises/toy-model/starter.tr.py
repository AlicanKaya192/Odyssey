import re


def toy_model(prompt, text):
    return "unknown"


PROMPT = """Classify.
- shipping: parcel, courier
- returns: return, back
- refunds: refund, money"""
for text in ["Where is my parcel?", "I want my money back.",
             "The zip broke."]:
    print(toy_model(PROMPT, text))
