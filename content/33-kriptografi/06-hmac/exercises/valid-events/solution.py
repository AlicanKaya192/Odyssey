import hashlib
import hmac


def make_tag(key_hex, message):
    key = bytes.fromhex(key_hex)
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()


def valid_events(key_hex, events):
    bodies = set()
    for body, tag in events:
        if hmac.compare_digest(make_tag(key_hex, body), tag):
            bodies.add(body)
    return sorted(bodies)

key = "5f0e2b9ac4d17733e1a6082cb94d1122"
good1 = make_tag(key, "order 1")
good2 = make_tag(key, "order 2")
events = [
    ["order 2", good2],
    ["order 1", good1],
    ["order 3", "deadbeef"],
    ["order 1", good2],
]
for body in valid_events(key, events):
    print(body)
