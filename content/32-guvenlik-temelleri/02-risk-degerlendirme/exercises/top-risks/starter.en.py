def top_risks(register, n):
    rows = []
    # [name, score] for every risk, then sort and take the first n
    return rows

register = [
    {"name": "laptop lost", "likelihood": 4, "impact": 3},
    {"name": "db leak", "likelihood": 2, "impact": 5},
    {"name": "site down", "likelihood": 3, "impact": 3},
    {"name": "ransomware", "likelihood": 3, "impact": 5},
    {"name": "phishing", "likelihood": 5, "impact": 2},
]
for row in top_risks(register, 3):
    print(row)
