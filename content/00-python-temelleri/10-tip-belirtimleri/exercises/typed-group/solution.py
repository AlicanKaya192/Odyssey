def group_by_city(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for row in rows:
        city = row["city"]
        if city not in result:
            result[city] = []
        result[city].append(row["name"])
    return result


def first_name(rows: list[dict[str, str]], city: str) -> str | None:
    for row in rows:
        if row["city"] == city:
            return row["name"]
    return None


people = [
    {"name": "Ada", "city": "London"},
    {"name": "Alan", "city": "London"},
    {"name": "Grace", "city": "New York"},
]

print(group_by_city(people))
print(first_name(people, "New York"))
print(first_name(people, "Paris"))
