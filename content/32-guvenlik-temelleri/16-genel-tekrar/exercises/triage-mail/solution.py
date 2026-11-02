from urllib.parse import urlsplit


def belongs(host, domain):
    return host is not None and (host == domain or host.endswith("." + domain))


def triage_mail(mails, domain, threshold):
    found = []
    for mail in mails:
        score = 0
        sender = mail["from"].rsplit("@", 1)[-1].lower()
        if not belongs(sender, domain):
            score += 3
        hosts = [urlsplit(url).hostname for url in mail.get("links", [])]
        if any(not belongs(host, domain) for host in hosts):
            score += 2
        if mail.get("urgent"):
            score += 2
        if mail.get("asks_password"):
            score += 3
        if score >= threshold:
            found.append([mail["id"], score])
    return sorted(found, key=lambda m: (-m[1], m[0]))

mails = [
    {"id": "m1", "from": "it@school.example",
     "links": ["https://login.school.example/"]},
    {"id": "m2", "from": "help@school-example.test",
     "links": ["https://school-example.test/reset"],
     "urgent": True, "asks_password": True},
    {"id": "m3", "from": "boss@school.example", "urgent": True},
    {"id": "m4", "from": "news@school.example",
     "links": ["https://school.example.evil.test/x"],
     "asks_password": True},
]
for mail_id, score in triage_mail(mails, "school.example", 4):
    print(mail_id, score)
