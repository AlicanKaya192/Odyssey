import hashlib
import json


def digest(data, n):
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h, "big") % n


def tbs(cert):
    body = {k: v for k, v in cert.items() if k != "signature"}
    return json.dumps(body, sort_keys=True).encode()


def check_signature(cert, e, n):
    return pow(cert["signature"], e, n) == digest(tbs(cert), n)


def verify_chain(chain, trusted):
    for cert, parent in zip(chain, chain[1:]):
        if cert["issuer"] != parent["subject"]:
            return "issuer mismatch"
        if not check_signature(cert, parent["e"], parent["n"]):
            return "bad signature"
    top = chain[-1]
    if trusted.get(top["subject"]) != [top["e"], top["n"]]:
        return "untrusted root"
    return "ok"

root = {'subject': 'Toy Root CA', 'e': 65537, 'n': 10967535067, 'issuer': 'Toy Root CA', 'signature': 9043170529}
mid = {'subject': 'Toy Issuing CA', 'e': 65537, 'n': 10962927607, 'issuer': 'Toy Root CA', 'signature': 1071094906}
site = {'subject': '*.example.test', 'e': 65537, 'n': 10968372731, 'not_before': '2026-01-01', 'not_after': '2026-12-31', 'issuer': 'Toy Issuing CA', 'signature': 5942274013}
trusted = {"Toy Root CA": [65537, 10967535067]}
print(verify_chain([site, mid, root], trusted))
print(verify_chain([site, mid, root], {}))
