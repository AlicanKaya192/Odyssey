`students.csv`'nin ilk satırı başlık: `name,house`. Dosyayı `csv.DictReader` ile oku ve öğrencileri **binaya göre** sıralayıp `Harry is in Gryffindor` biçiminde yaz. Sıralamada `key=lambda ...` kullan. Aynı binadaki öğrenciler dosyadaki sırayla kalır (`sorted` eşitlerin sırasını değiştirmez).

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın ve dosyan denetlenir):

```text
$ python cozum.py
Hermione is in Gryffindor
Harry is in Gryffindor
Cedric is in Hufflepuff
Luna is in Ravenclaw
Draco is in Slytherin
```
