argparse ile komut satırından iki seçenek alan bir program yaz:

- `-n` ya da `--number`: kaç kez (tam sayı, varsayılan 1)
- `-s` ya da `--sound`: hangi ses (varsayılan `meow`)

Program sesi o kadar kez, her satırda bir tane yazar. Seçenekler herhangi bir sırada gelebilir. `-n dog` gibi geçersiz bir sayıda argparse kendi iletisini yazıp programı 2 koduyla bitirmeli; bunu elle yazma, `type=int` yapıyor.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py -n 2 -s purr
purr
purr
```
