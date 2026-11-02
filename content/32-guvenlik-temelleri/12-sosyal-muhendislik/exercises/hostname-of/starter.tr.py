def hostname_of(url):
    return url.split("/")[2]

for url in ["https://login.school.example/reset", "https://school.example@evil.test/x",
            "http://files.example:8443/a", "HTTPS://Login.School.Example/"]:
    print(hostname_of(url))
