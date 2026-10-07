import csv
import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# rows: id, title, price (float), author_name, tags (joined with "|")


# Write to books.csv: writeheader + writerows


# Open the file again and print its contents
