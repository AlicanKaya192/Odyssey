import html
import re

STOP = {"the", "a", "is", "and"}


def clean_tokens(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return [w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP]

print(clean_tokens("<p>The lid is <b>NOT</b> tight &amp; leaks</p>"))
