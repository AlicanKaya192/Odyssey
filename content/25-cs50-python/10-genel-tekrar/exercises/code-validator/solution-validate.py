import re


def main():
    if is_valid(input("Code: ")):
        print("Valid")
    else:
        print("Invalid")


def is_valid(code):
    return re.fullmatch(r"[A-Z]{2}-[1-9][0-9]{3}", code) is not None


if __name__ == "__main__":
    main()
