def main():
    name = input("Name: ")
    print(initials(name))


def initials(name):
    return "".join(word[0].upper() for word in name.split())


if __name__ == "__main__":
    main()
