class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"


def main():
    title = input("Title: ")
    author = input("Author: ")
    book = Book(title, author)
    print(book)


if __name__ == "__main__":
    main()
