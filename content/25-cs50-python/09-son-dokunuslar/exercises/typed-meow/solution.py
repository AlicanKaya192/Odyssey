def meow(n: int) -> str:
    return "meow\n" * n


def main():
    number: int = int(input("Number: "))
    meows: str = meow(number)
    print(meows, end="")


if __name__ == "__main__":
    main()
