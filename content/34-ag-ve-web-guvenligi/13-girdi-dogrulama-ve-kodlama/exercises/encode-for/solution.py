import html
import json
from urllib.parse import quote


def encode_for(context, value):
    if context == "html":
        return html.escape(value)
    if context == "url":
        return quote(value, safe="")
    if context == "json":
        return json.dumps(value)
    return None

value = 'a&b "c" <d>'
for context in ["html", "url", "json", "sql"]:
    print(context, encode_for(context, value))
