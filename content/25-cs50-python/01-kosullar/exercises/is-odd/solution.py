def main():
    n = int(input("n: "))
    if is_odd(n):
        print("Odd")
    else:
        print("Even")


def is_odd(n):
    return n % 2 == 1


main()
