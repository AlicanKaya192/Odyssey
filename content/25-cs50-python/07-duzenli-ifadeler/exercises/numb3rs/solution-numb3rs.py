import re


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    if not re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip):
        return False
    for number in ip.split("."):
        if int(number) > 255:
            return False
    return True


if __name__ == "__main__":
    main()
