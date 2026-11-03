import hashlib
import json


def digest(data, n):
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h, "big") % n


def check_signature(cert, e, n):
    data = json.dumps(cert, sort_keys=True).encode()
    return pow(cert["signature"], e, n) == digest(data, n)

cert = {'subject': 'shop.example.test', 'e': 65537, 'n': 10968372731, 'not_before': '2026-01-01', 'not_after': '2026-12-31', 'issuer': 'Toy Root CA', 'signature': 9063980524}
print(check_signature(cert, 65537, 10967535067))
print(check_signature(dict(cert, n=12345), 65537, 10967535067))
