import html
import json
from urllib.parse import quote


def encode_for(context, value):
    return html.escape(value)

value = 'a&b "c" <d>'
for context in ["html", "url", "json", "sql"]:
    print(context, encode_for(context, value))
