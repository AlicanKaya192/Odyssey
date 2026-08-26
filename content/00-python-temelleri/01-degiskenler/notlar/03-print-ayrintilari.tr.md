`print()` ilk günden kullandığın fonksiyon ama birkaç ayarı var ve bunları bilmek işini kolaylaştırıyor.

## Virgülle ayırmak

Virgül kullanınca Python değerleri yan yana yazar ve **araya kendisi boşluk koyar**. Tipler farklı olsa bile sorun çıkmaz:

```python
name = "Alican"
year = 2001
print(name, year)      # Alican 2001
```

Bu, `+` ile birleştirmeye göre hem daha kısa hem daha güvenli. `+` kullanmak isteseydin sayıyı önce `str()` ile çevirmen gerekirdi.

## Ayırıcıyı değiştirmek: sep

Araya konan boşluğu beğenmiyorsan `sep` ile değiştirebilirsin:

```python
print("2026", "08", "26", sep="-")    # 2026-08-26
print("a", "b", "c", sep="")          # abc
```

## Satır sonunu değiştirmek: end

`print()` varsayılan olarak sonuna alt satıra geçme karakteri koyar. `end` ile bunu değiştirebilirsin:

```python
print("yükleniyor", end="")
print("...")          # yükleniyor...
```

Aynı satırda devam etmek istediğinde işine yarar.

## f-string ile biçimlendirme

Metnin içine değişken yerleştirmenin en temiz yolu:

```python
name = "Alican"
age = 25
print(f"{name} {age} yaşında.")
```

f-string içinde işlem de yapabilirsin:

```python
print(f"5 yıl sonra {age + 5} olacak.")
```

Ondalıklı sayılarda basamak sayısını sınırlamak için iki nokta ve biçim kodu kullanılır:

```python
pi = 3.14159265
print(f"Pi yaklaşık {pi:.2f}")     # Pi yaklaşık 3.14
```

Bu `.2f` gösterimi tabloları ve raporları düzenli yazdırırken sık işine yarayacak.
