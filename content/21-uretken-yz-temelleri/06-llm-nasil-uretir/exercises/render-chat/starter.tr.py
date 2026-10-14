def render_chat(messages):
    return ""


messages = [
    {"role": "system", "content": "be brief ."},
    {"role": "user", "content": "hi"},
]
print(render_chat(messages))
