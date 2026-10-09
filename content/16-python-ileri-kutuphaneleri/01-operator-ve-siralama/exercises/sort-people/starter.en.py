def sort_people(people):
    ordered = sorted(people, key=lambda p: p["age"])
    return [p["name"] for p in ordered]

people = [{"name": "Ada", "age": 36}, {"name": "Alan", "age": 41},
          {"name": "Grace", "age": 36}, {"name": "Bob", "age": 41}]
print(sort_people(people))
