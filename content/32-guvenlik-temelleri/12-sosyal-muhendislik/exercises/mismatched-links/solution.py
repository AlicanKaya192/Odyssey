from urllib.parse import urlsplit


def text_host(text):
    text = text.strip().lower()
    for prefix in ("https://", "http://"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text.split("/")[0]


def mismatched_links(links):
    result = []
    for text, href in links:
        if "." not in text:
            continue
        if text_host(text) != (urlsplit(href).hostname or ""):
            result.append(href)
    return result

links = [
    ["login.school.example", "https://login.school.example/a"],
    ["https://bank.example/pay", "https://bank-example.test/pay"],
    ["Click here", "https://evil.test/x"],
    ["SCHOOL.EXAMPLE", "https://school.example/"],
]
for href in mismatched_links(links):
    print(href)
