import base64
import hashlib
import hmac
import json


def make_token(claims, key):
    body = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode()
    return body + "." + hmac.new(key.encode(), body.encode(), hashlib.sha256).hexdigest()


def verify_token(token, key):
    body, signature = token.split(".")
    return json.loads(base64.urlsafe_b64decode(body))

token = make_token({"sub": "ada", "role": "user"}, "toy-key")
print(verify_token(token, "toy-key"))
body, signature = token.split(".")
fake = base64.urlsafe_b64encode(b'{"sub": "ada", "role": "admin"}').decode()
print(verify_token(fake + "." + signature, "toy-key"))
print(verify_token(token, "other-key"))
print(verify_token("no-dot-here", "toy-key"))
