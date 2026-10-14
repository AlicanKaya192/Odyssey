def render_rules(rules):
    return ""


print(render_rules({"max_words": 15, "must_include": ["tent", "zip"]}))
print("---")
print(render_rules({"max_sentences": 2}))
