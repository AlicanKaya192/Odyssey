def main():
    length = int(input("Minimum length: "))
    for i, word in enumerate(long_words("words.txt", length), start=1):
        print(f"{i}. {word}")


def long_words(path, length):
    with open(path) as file:
        for line in file:
            for word in line.split():
                if len(word) >= length:
                    yield word


if __name__ == "__main__":
    main()
