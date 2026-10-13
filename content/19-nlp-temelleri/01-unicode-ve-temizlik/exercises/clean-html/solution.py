import html
import re


def clean_html(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split())

print(clean_html("<p>Great &amp; cheap</p>"))
print(clean_html("Fast<br>delivery,   <b>well</b> packed"))
print(clean_html("5 &lt; 7"))
