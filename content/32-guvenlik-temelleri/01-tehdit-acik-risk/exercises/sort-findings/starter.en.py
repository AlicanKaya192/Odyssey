def sort_findings(findings):
    ordered = sorted(findings, key=lambda f: f[1], reverse=True)
    return [f[0] for f in ordered]

findings = [["xss in search", 6.1], ["sql in login", 9.8], ["debug page", 6.1],
            ["old tls", 5.9], ["admin panel", 9.8]]
for name in sort_findings(findings):
    print(name)
