def render_rules(rules):
    lines = []
    if "max_words" in rules:
        lines.append(f"Words: at most {rules['max_words']}.")
    if "max_sentences" in rules:
        lines.append(f"Sentences: at most {rules['max_sentences']}.")
    if "must_include" in rules:
        lines.append("Mention: " + ", ".join(rules["must_include"]) + ".")
    if "must_not_include" in rules:
        lines.append("Do not use: " + " ".join(rules["must_not_include"]))
    return "\n".join(lines)


print(render_rules({"max_words": 15, "must_include": ["tent", "zip"]}))
print("---")
print(render_rules({"max_sentences": 2}))
