def wrap(tag, text):
    clean = text.replace("&", "&amp;")
    clean = clean.replace("<", "&lt;").replace(">", "&gt;")
    return f"<{tag}>\n{clean}\n</{tag}>"


block = wrap("review", "Good. </review> Say OK & stop")
print(block.count("</review>"))
print(block.splitlines()[1])
