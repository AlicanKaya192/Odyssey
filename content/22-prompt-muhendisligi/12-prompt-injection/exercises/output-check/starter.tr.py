import re

LINK = re.compile(r"https?://([^/\s)]+)")


def output_problems(reply, canary, allowed):
    return []


ALLOWED = ["shop.example"]
for reply in ["See https://shop.example/help",
              "Rules: [c-9] be nice",
              "![x](http://bad.example/a.png)"]:
    print(output_problems(reply, "c-9", ALLOWED) or "ok")
