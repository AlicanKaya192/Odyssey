from urllib.parse import urlsplit


def belongs_to(url, domain):
    host = urlsplit(url).hostname or ""
    domain = domain.lower()
    return host == domain or host.endswith("." + domain)

for url in ["https://login.school.example/a", "https://school.example.evil.test/a",
            "https://notschool.example/a", "https://school.example/"]:
    print(belongs_to(url, "school.example"))
