import html
from urllib.parse import urlsplit


def safe_link(url, label):
    if urlsplit(url).scheme not in ("http", "https"):
        return html.escape(label)
    return f'<a href="{html.escape(url)}">{html.escape(label)}</a>'

print(safe_link("https://a.example/", "docs"))
print(safe_link("javascript:go()", "<b>click</b>"))
print(safe_link("http://a.example/?p=1&q", "x"))
