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


def date_status(cert, today):
    if today < cert["not_before"]:
        return "not yet valid"
    if today > cert["not_after"]:
        return "expired"
    return "ok"


def host_matches(pattern, host):
    if pattern.startswith("*."):
        suffix = pattern[1:]
        rest = host[: -len(suffix)]
        return host.endswith(suffix) and rest != "" and "." not in rest
    return pattern == host


def check_site(chain, trusted, host, today):
    result = verify_chain(chain, trusted)
    if result != "ok":
        return result
    return "ok"

chain = [{'subject': '*.example.test', 'e': 65537, 'n': 10968372731, 'not_before': '2026-01-01', 'not_after': '2026-12-31', 'issuer': 'Toy Issuing CA', 'signature': 5942274013}, {'subject': 'Toy Issuing CA', 'e': 65537, 'n': 10962927607, 'issuer': 'Toy Root CA', 'signature': 1071094906}, {'subject': 'Toy Root CA', 'e': 65537, 'n': 10967535067, 'issuer': 'Toy Root CA', 'signature': 9043170529}]
trusted = {"Toy Root CA": [65537, 10967535067]}
print(check_site(chain, trusted, "shop.example.test", "2026-11-03"))
print(check_site(chain, trusted, "shop.example.test", "2027-02-01"))
print(check_site(chain, trusted, "bank.other.test", "2026-11-03"))
