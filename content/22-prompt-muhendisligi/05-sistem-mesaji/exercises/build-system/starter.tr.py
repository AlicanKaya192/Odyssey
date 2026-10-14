def build_system(settings):
    return ""


print(build_system({"role": "You help hikers.", "tone": "Be brief.",
                    "rules": ["No promises.", "Be polite."]}))
print("---")
print(build_system({"role": "You help hikers.", "tone": "Be brief."}))
