"""The lesson's schema and row check."""

SCHEMA = {
    "tenure": {"min": 1, "max": 72},
    "monthly_fee": {"min": 5, "max": 100},
    "support_calls": {"min": 0, "max": 10},
    "usage_hours": {"min": 0, "max": 100},
    "plan": {"allowed": ["basic", "pro"]},
    "churned": {"allowed": [0, 1]},
}


def check_row(row, schema):
    """Return a list of problems; an empty list means the row is sound."""
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
    return problems
