import html
import re


def clean_html(text):
    return text

print(clean_html("<p>Great &amp; cheap</p>"))
print(clean_html("Fast<br>delivery,   <b>well</b> packed"))
print(clean_html("5 &lt; 7"))
