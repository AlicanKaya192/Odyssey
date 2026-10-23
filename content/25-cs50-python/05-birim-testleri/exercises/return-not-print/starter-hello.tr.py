def main():
    name = input("What's your name? ")
    hello(name)


def hello(to="world"):
    # Selamı yazdırmak yerine döndür
    print("hello,", to)


if __name__ == "__main__":
    main()
