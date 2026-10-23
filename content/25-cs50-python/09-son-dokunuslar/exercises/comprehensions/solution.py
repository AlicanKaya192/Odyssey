def shout(*words):
    return [word.upper() for word in words]


def gryffindors(students):
    return sorted(s["name"] for s in students if s["house"] == "Gryffindor")


def ranks(names):
    return {name: i for i, name in enumerate(names, start=1)}
