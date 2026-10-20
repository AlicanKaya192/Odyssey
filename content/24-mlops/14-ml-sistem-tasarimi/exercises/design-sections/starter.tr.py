def missing_sections(doc, required):
    # Once basliklari topla, sonra eksikleri bul.
    pass


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
