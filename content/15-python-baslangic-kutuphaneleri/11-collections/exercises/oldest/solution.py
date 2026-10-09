from collections import namedtuple

Person = namedtuple("Person", ["name", "age"])


def oldest(lines):
    people = []
    for line in lines:
        name, age = line.split(",")
        people.append(Person(name, int(age)))
    return max(people, key=lambda p: p.age).name

print(oldest(["Ada,36", "Alan,41", "Grace,85", "Linus,56"]))
