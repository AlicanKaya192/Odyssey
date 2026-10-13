import html
import re

STOP = {"the", "a", "is", "and"}


def clean_tokens(text):
    return []

print(clean_tokens("<p>The lid is <b>NOT</b> tight &amp; leaks</p>"))
