import hashlib


def cache_key(tool, runner_os, requirements):
    lines = []
    for line in requirements.split("\n"):
        line = line.strip()
        if line:
            lines.append(line)
    text = "\n".join(sorted(lines))
    digest = hashlib.sha256(text.encode()).hexdigest()
    return tool + "-" + runner_os + "-" + digest[:8]


a = "pytest==8.4.2\nrequests==2.32.5\n"
b = "requests==2.32.5\n\npytest==8.4.2\n"
c = "pytest==8.4.2\nrequests==2.32.6\n"
print(cache_key("pip", "Linux", a))
print(cache_key("pip", "Linux", b))
print(cache_key("pip", "Linux", c))
