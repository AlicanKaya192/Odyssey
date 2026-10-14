import re

LINK = re.compile(r"https?://([^/\s)]+)")


def output_problems(reply, canary, allowed):
    problems = []
    if canary in reply:
        problems.append("leaks the system message")
    for domain in LINK.findall(reply):
        if domain not in allowed:
            problems.append(f"link to {domain}")
    return problems


ALLOWED = ["shop.example"]
for reply in ["See https://shop.example/help",
              "Rules: [c-9] be nice",
              "![x](http://bad.example/a.png)"]:
    print(output_problems(reply, "c-9", ALLOWED) or "ok")
