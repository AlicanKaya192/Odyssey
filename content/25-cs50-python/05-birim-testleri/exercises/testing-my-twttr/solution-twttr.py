def main():
    word = input("Input: ")
    print(shorten(word))


def shorten(word):
    result = ""
    for c in word:
        if c.lower() not in "aeiou":
            result += c
    return result


if __name__ == "__main__":
    main()
