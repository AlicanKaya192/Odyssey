def main():
    name = input("What's your name? ")
    hello(name)


def hello(to="world"):
    # Return the greeting instead of printing it
    print("hello,", to)


if __name__ == "__main__":
    main()
