Hafta 6'da geçen her şey tek sayfada.

## Dosya açmak

| Yazım | Ne yapar |
|---|---|
| `open("names.txt")` | okumak için açar (`"r"` varsayılan) |
| `open("names.txt", "w")` | yazmak için açar; dosya varsa **içini siler** |
| `open("names.txt", "a")` | sonuna eklemek için açar; yoksa oluşturur |
| `with open(...) as file:` | blok bitince dosyayı kendiliğinden kapatır |
| `file.close()` | `with` kullanmıyorsan kapatmak için |

## Yazmak ve okumak

| Yazım | Ne yapar |
|---|---|
| `file.write(f"{name}\n")` | metni yazar; satır sonunu **sen** eklersin |
| `file.readlines()` | bütün satırlar, liste olarak (her biri `\n` ile biter) |
| `for line in file:` | dosyayı satır satır gezer |
| `line.rstrip()` | sağdaki boşlukları ve `\n`'yi atar |
| `sorted(file)` | satırları sıralı verir |

## Sıralamak

| Yazım | Ne yapar |
|---|---|
| `sorted(names)` | abece sırası (büyük harfler önce: `"C"` `"a"`'dan önce) |
| `sorted(names, reverse=True)` | ters sıra |
| `sorted(students, key=get_name)` | her öğe için `get_name(öğe)`'nin değerine göre |
| `key=lambda s: s["name"]` | aynısı, adsız fonksiyonla |

`sorted` kararlıdır: değeri eşit öğeler (aynı binadaki iki öğrenci) girdideki
sıralarını korur.

## CSV

`import csv` ile:

| Yazım | Ne yapar |
|---|---|
| `csv.reader(file)` | her satır bir **liste**; tırnaklı alanı doğru okur |
| `csv.DictReader(file)` | ilk satır başlık; her satır bir **sözlük** (`row["name"]`) |
| `csv.writer(file)` | `writer.writerow([name, home])` |
| `csv.DictWriter(file, fieldnames=[...])` | `writer.writerow({...})`; sütun sırası `fieldnames`'ten |
| `writer.writeheader()` | `DictWriter`'ın başlık satırını yazar |

Windows'ta CSV'ye yazarken dosyayı `open("students.csv", "a", newline="")`
ile aç; yoksa satırların arasına boş satır girer.

## Resimler (Pillow)

`from PIL import Image` ile:

| Yazım | Ne yapar |
|---|---|
| `Image.open("costume1.gif")` | resmi açar |
| `image.size` | `(genişlik, yükseklik)` |
| `image.save("out.png")` | uzantıya göre biçimi seçip kaydeder |
| `images[0].save("x.gif", save_all=True, append_images=images[1:], duration=200, loop=0)` | hareketli GIF |
| `ImageOps.fit(image, size)` | resmi boyuta getirip ortadan kırpar (`from PIL import ImageOps`) |
| `photo.paste(shirt, shirt)` | `shirt`'ü üstüne koyar; ikincisi saydamlık maskesi |
