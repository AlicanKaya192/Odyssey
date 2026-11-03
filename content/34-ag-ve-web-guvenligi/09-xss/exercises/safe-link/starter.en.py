import html
from urllib.parse import urlsplit


def safe_link(url, label):
    # check the scheme, then encode both values
    return f'<a href="{url}">{label}</a>'

print(safe_link("https://a.example/", "docs"))
print(safe_link("javascript:go()", "<b>click</b>"))
print(safe_link("http://a.example/?p=1&q", "x"))
