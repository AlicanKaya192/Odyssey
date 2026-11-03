import hashlib
import json


def digest(data, n):
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h, "big") % n


def tbs(cert):
    body = {k: v for k, v in cert.items() if k != "signature"}
    return json.dumps(body, sort_keys=True).encode()


def verify_message(cert, ca_e, ca_n, message, signature):
    if pow(signature, cert["e"], cert["n"]) != digest(message.encode(), cert["n"]):
        return "bad signature"
    return "ok"

cert = {'subject': 'shop.example.test', 'e': 65537, 'n': 10968372731, 'issuer': 'Toy Root CA', 'signature': 5025653789}
ca_n = 10967535067
print(verify_message(cert, 65537, ca_n, "order 42 shipped", 492434088))
print(verify_message(cert, 65537, ca_n, "order 43 shipped", 492434088))
print(verify_message(dict(cert, subject="bank.example.test"), 65537, ca_n, "order 42 shipped", 492434088))
