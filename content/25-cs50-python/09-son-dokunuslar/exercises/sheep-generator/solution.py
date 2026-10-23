def main():
    n = int(input("What's n? "))
    for line in sheep(n):
        print(line)


def sheep(n):
    for i in range(1, n + 1):
        yield f"{i} sheep"


if __name__ == "__main__":
    main()
