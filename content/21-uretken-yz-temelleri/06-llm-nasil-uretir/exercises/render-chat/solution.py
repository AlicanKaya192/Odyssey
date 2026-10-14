def render_chat(messages):
    parts = []
    for m in messages:
        parts.append("<" + m["role"] + ">")
        parts.append(m["content"])
    parts.append("<assistant>")
    return " ".join(parts)


messages = [
    {"role": "system", "content": "be brief ."},
    {"role": "user", "content": "hi"},
]
print(render_chat(messages))
