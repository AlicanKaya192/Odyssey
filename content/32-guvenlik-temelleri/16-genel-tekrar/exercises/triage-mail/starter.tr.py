from urllib.parse import urlsplit


def belongs(host, domain):
    return host is not None and (host == domain or host.endswith("." + domain))


def triage_mail(mails, domain, threshold):
    found = []
    for mail in mails:
        score = 0
        if domain not in mail["from"]:
            score += 3
        if mail["urgent"]:
            score += 2
        if score >= threshold:
            found.append([mail["id"], score])
    return found

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
