def build_system(settings):
    lines = [settings["role"], settings["tone"]]
    rules = settings.get("rules", [])
    if rules:
        lines.append("Rules:")
        lines += [f"{i}. {rule}" for i, rule in enumerate(rules, 1)]
    return "\n".join(lines)


print(build_system({"role": "You help hikers.", "tone": "Be brief.",
                    "rules": ["No promises.", "Be polite."]}))
print("---")
print(build_system({"role": "You help hikers.", "tone": "Be brief."}))
