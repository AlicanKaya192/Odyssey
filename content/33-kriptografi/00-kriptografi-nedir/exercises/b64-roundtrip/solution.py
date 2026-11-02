import base64


def b64_roundtrip(text):
    encoded = base64.b64encode(text.encode()).decode()
    decoded = base64.b64decode(encoded).decode()
    return [encoded, decoded]

encoded, decoded = b64_roundtrip("meet at noon")
print(encoded)
print(decoded)
print(type(encoded).__name__, type(decoded).__name__)
