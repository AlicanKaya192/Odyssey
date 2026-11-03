def open_admin_ports(rules, admin_ports):
    found = []
    for r in rules:
        if r["port"] in admin_ports and r["source"] == "0.0.0.0/0":
            found.append(r["port"])
    return found

RULES = [
    {"port": 443, "source": "0.0.0.0/0"},
    {"port": 22, "source": "0.0.0.0/0"},
    {"port": 5432, "source": "10.0.0.0/16"},
    {"port": 3389, "source": "::/0"},
    {"port": 22, "source": "::/0"},
]
print(open_admin_ports(RULES, [22, 3389, 5432]))
