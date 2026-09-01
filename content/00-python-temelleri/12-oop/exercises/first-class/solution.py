class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def is_long(self):
        return self.pages >= 300


long_book = Book("Ulysses", 730)
short_book = Book("Notes", 120)

print(long_book.title)
print(long_book.is_long())
print(short_book.title)
print(short_book.is_long())
