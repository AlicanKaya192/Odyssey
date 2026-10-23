Ders on haftanın yazımlarını topluyor; bu not hata iletilerini. Bir program
düştüğünde iletinin **son satırını** oku: önce hatanın türü, sonra ne olduğu.
İletiler bu bilgisayarda Python 3.14'te ölçüldü.

## Sık karşılaşılan hatalar

| Son satır | Ne oldu | Hafta |
|---|---|---|
| `NameError: name 'x' is not defined` | tanımlanmamış (ya da yanlış yazılmış) bir ad | 0 |
| `TypeError: can only concatenate str (not "int") to str` | dize ile sayıyı `+` ile birleştirmek; `str(n)` ya da f-string | 0 |
| `ValueError: invalid literal for int() with base 10: 'cat'` | sayıya çevrilemeyen dize; `try`/`except ValueError` | 3 |
| `IndexError: list index out of range` | listede olmayan bir konum | 2 |
| `KeyError: 'b'` | sözlükte olmayan bir anahtar; `in` ya da `.get` | 2 |
| `FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'` | olmayan bir dosya | 6 |
| `AttributeError: 'str' object has no attribute 'append'` | o türde olmayan bir metot ya da nitelik | 8 |
| `UnboundLocalError: cannot access local variable ...` | fonksiyonda genel değişkene atamak; `global` | 9 |
| `StopIteration` | üretecin (yineleyicinin) değerleri bitti | 9 |

## Yığın dökümünü okumak

Hafta 9'daki banka programının dökümü:

```text
Traceback (most recent call last):
  File "bank.py", line 19, in <module>
    main()
    ~~~~^^
  File "bank.py", line 5, in main
    deposit(100)
    ~~~~~~~^^^^^
  File "bank.py", line 11, in deposit
    balance += n
    ^^^^^^^
UnboundLocalError: cannot access local variable 'balance' where it is not
associated with a value
```

- Döküm dıştan içe: en üstte programın başladığı yer, en altta hatanın
  çıktığı satır.
- Kendi dosyanın en alttaki satırına bak; hata çoğunlukla oradadır ya da
  oraya gelen değerdedir.
- `^^^^` işaretleri satırın hangi parçasının hata verdiğini gösterir.

## Hangi aracı ne zaman

| İş | Araç |
|---|---|
| Kullanıcı geçersiz bir şey yazabilir | `while True` + `try`/`except` |
| Program yanlış kullanıldı | `sys.exit("Usage: ...")` |
| Kendi fonksiyonun geçersiz girdi aldı | `raise ValueError("...")` |
| Bir değerin biçimi | `re.fullmatch(r"...", s)` |
| Birbirine ait veri ve işlev | sınıf |
| Bir fonksiyonun doğru çalıştığı | `pytest`, `assert` |
| Komut satırında birkaç seçenek | `argparse` |
| Çok büyük ya da sonu belirsiz veri | üreteç, `yield` |
