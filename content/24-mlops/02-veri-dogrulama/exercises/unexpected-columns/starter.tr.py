def check_row(row, schema):
    # Dersteki denetimler + semada olmayan sutunlar icin "unexpected".
    pass


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
