from urllib.parse import urlsplit


def mismatched_links(links):
    result = []
    # compare the two servers of every link
    return result

links = [
    ["login.school.example", "https://login.school.example/a"],
    ["https://bank.example/pay", "https://bank-example.test/pay"],
    ["Click here", "https://evil.test/x"],
    ["SCHOOL.EXAMPLE", "https://school.example/"],
]
for href in mismatched_links(links):
    print(href)
