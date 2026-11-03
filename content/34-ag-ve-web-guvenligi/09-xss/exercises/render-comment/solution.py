import html


def render_comment(author, text):
    return f"<p><b>{html.escape(author)}</b>: {html.escape(text)}</p>"

print(render_comment("ada", "1 < 2 & ok"))
print(render_comment("<b>bob</b>", "hi"))
