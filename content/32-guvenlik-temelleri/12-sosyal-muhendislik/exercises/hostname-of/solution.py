from urllib.parse import urlsplit


def hostname_of(url):
    return urlsplit(url).hostname or ""

for url in ["https://login.school.example/reset", "https://school.example@evil.test/x",
            "http://files.example:8443/a", "HTTPS://Login.School.Example/"]:
    print(hostname_of(url))
