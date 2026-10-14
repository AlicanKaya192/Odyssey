def escape_braces(text):
    return text.replace("{", "{{").replace("}", "}}")


example = escape_braces('{"category": "<name>"}')
template = "Answer as JSON: " + example + "\nMessage: {message}"
print(template.format(message="Hi"))
