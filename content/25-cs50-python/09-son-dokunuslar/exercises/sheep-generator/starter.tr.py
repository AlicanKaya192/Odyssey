def main():
    n = int(input("What's n? "))
    for line in sheep(n):
        print(line)


def sheep(n):
    flock = []
    for i in range(1, n + 1):
        flock.append(f"{i} sheep")
    return flock


if __name__ == "__main__":
    main()
