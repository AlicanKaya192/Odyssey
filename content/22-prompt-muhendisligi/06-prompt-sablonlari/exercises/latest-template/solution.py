def render_latest(templates, name, values):
    versions = templates.get(name, {})
    if not versions:
        return [0, ""]
    latest = max(versions, key=int)
    return [int(latest), versions[latest].format(**values)]


TEMPLATES = {
    "classify": {"1": "Category of: {message}",
                 "2": "One category for: {message}",
                 "10": "Pick one category: {message}"},
    "reply": {"1": "Reply to {name}: {message}"},
}
version, text = render_latest(TEMPLATES, "classify", {"message": "Hi"})
print(version)
print(text)
print(render_latest(TEMPLATES, "summary", {}))
