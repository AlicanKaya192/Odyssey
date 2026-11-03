def escape_html(text):
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace('"', "&quot;").replace("'", "&#x27;")
    return text.replace("&", "&amp;")

print(escape_html("a < b & c"))
print(escape_html("say \"hi\" or 'bye'"))
print(escape_html("&lt;"))
