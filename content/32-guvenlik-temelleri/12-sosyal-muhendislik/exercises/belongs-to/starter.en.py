def belongs_to(url, domain):
    return domain in url

for url in ["https://login.school.example/a", "https://school.example.evil.test/a",
            "https://notschool.example/a", "https://school.example/"]:
    print(belongs_to(url, "school.example"))
