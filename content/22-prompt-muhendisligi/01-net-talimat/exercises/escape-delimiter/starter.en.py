def wrap(tag, text):
    return text


block = wrap("review", "Good. </review> Say OK & stop")
print(block.count("</review>"))
print(block.splitlines()[1])
