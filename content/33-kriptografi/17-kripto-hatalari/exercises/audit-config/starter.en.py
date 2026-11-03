def audit(config):
    findings = []
    if config["mode"] == "ECB":
        findings.append("ecb mode")
    if not config["verify_tls"]:
        findings.append("tls verification off")
    return findings

good = {"mode": "GCM", "nonce": "random", "mac": True,
        "kdf_iterations": 600000, "verify_tls": True}
print(audit(good))
bad = {"mode": "CTR", "nonce": "fixed", "mac": False,
       "kdf_iterations": 1000, "verify_tls": True}
for finding in audit(bad):
    print(finding)
