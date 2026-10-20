def check_row(row, schema):
    problems = []
    for column, rule in schema.items():
        value = row.get(column)
        if value is None:
            problems.append(f"{column}: missing")
        elif "allowed" in rule:
            if value not in rule["allowed"]:
                problems.append(f"{column}: {value!r} is not allowed")
        elif not isinstance(value, (int, float)):
            problems.append(f"{column}: {value!r} is not a number")
        elif not rule["min"] <= value <= rule["max"]:
            problems.append(f"{column}: {value} is out of range")
    for column in row:
        if column not in schema:
            problems.append(f"{column}: unexpected")
    return problems


SCHEMA = {"tenure": {"min": 1, "max": 72}, "plan": {"allowed": ["basic", "pro"]}}


def show(row):
    problems = check_row(row, SCHEMA)
    print(len(problems), "problem(s)")
    for problem in problems:
        print(" ", problem)


show({"tenure": 12, "plan": "pro"})
show({"tenure": 99, "plan": "Pro"})
show({"plan": "basic", "tenure_months": 12})
show({"tenure": "12", "plan": None, "note": "vip"})
