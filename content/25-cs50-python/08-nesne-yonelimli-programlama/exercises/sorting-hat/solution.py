import random


class Hat:
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    @classmethod
    def sort(cls, name):
        return f"{name} is in {random.choice(cls.houses)}"


def main():
    name = input("Name: ")
    print(Hat.sort(name))


if __name__ == "__main__":
    main()
