def missing_sections(doc, required):
    headings = set()
    for line in doc.splitlines():
        if line.startswith("## "):
            headings.add(line[3:].strip())
    return [name for name in required if name not in headings]


doc = """# Churn model
## Goal
Reduce churn.
## Data
Customer table.
## Serving
Nightly batch.
"""
required = ["Goal", "Data", "Model", "Serving", "Monitoring"]
print(missing_sections(doc, required))
print(missing_sections("## Goal\n## Model", ["Goal", "Model"]))
