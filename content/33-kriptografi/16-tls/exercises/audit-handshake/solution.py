STRONG_SUITES = [
    "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256",
]


def audit_handshake(info):
    problems = []
    if info["version"] not in ["TLSv1.3", "TLSv1.2"]:
        problems.append("old version")
    if info["suite"] not in STRONG_SUITES:
        problems.append("weak suite")
    if not info["cert_ok"]:
        problems.append("bad certificate")
    if not info["finished_ok"]:
        problems.append("bad finished")
    return problems

good = {"version": "TLSv1.3", "suite": "TLS_AES_128_GCM_SHA256",
        "cert_ok": True, "finished_ok": True}
print(audit_handshake(good))
old = dict(good, version="TLSv1.0", suite="TLS_RSA_WITH_RC4")
for problem in audit_handshake(old):
    print(problem)
