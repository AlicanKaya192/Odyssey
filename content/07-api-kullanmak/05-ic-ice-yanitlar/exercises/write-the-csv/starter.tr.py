import csv
import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# rows: id, title, price (float), author_name, tags ("|" ile)


# books.csv'ye yaz: writeheader + writerows


# Dosyayi yeniden ac ve icerigini yazdir
