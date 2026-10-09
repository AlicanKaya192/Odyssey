Derste `abracadabra` için kodları bulduk. Metni bu kodlarla bit dizisine
çevirmek kolay; asıl ilginç olan **geri çözmek**: bitler arasında ayraç
yok, nerede bir harfin bittiğini nasıl anlarız?

Cevap önek koşulu: hiçbir kod başka bir kodun başlangıcı değil. Bitleri
soldan okurken biriktirdiğin parça bir koda eşit olduğu an, o harf
**kesin** odur; daha uzun bir kodun başı olamaz.

```python
codes = {"a": "0", "b": "110", "c": "100", "d": "101", "r": "111"}

def encode(text):
    return "".join(codes[ch] for ch in text)

def decode(bits):
    reverse = {code: ch for ch, code in codes.items()}
    out, current = [], ""
    for bit in bits:
        current += bit
        if current in reverse:            # bir kod tamamlandı
            out.append(reverse[current])
            current = ""
    return "".join(out)

bits = encode("abracadabra")
print(bits, len(bits))
print(decode(bits))
```

```text
01101110100010101101110 23
abracadabra
```

Önek koşulu bozulsaydı (örneğin `a = 0`, `b = 01`), `01` dizisi "a sonra
bir şey" mi yoksa "b" mi belli olmazdı.

## Neden en iyi?

En seyrek iki harf ağaçta en derine, kardeş olarak konursa toplam bit sayısı
artmaz (değiştirme argümanı). Onları tek bir "harf" gibi birleştirince
kalan problem bir harf eksik aynı problem olur. Her adımda bu yapıldığı için
sonuç en iyi **önek kodu**dur.

**Not:** toplam bit sayısını bulmak için kodlara bile gerek yok: her
birleştirmede iki grubun sayıları toplamı kadar bit eklenir. Alıştırmada
bunu kullanacaksın.
