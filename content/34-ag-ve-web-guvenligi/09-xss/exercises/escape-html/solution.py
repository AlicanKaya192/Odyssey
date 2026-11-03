def escape_html(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text.replace('"', "&quot;").replace("'", "&#x27;")

print(escape_html("a < b & c"))
print(escape_html("say \"hi\" or 'bye'"))
print(escape_html("&lt;"))
