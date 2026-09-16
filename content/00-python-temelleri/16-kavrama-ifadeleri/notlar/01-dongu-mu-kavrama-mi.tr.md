Kavrama her zaman daha iyi değil. Karar vermek için tek bir soru yeter:
**bu satırı altı ay sonra okuyan biri ne yaptığını bir bakışta anlar mı?**

## Kavrama yaz

Üç işten birini yapıyorsan:

<figure class="fig anat">
  <div class="anat-row"><span>Dönüştürme</span><span>Her elemanı başka bir değere çevirmek: <code>[p * 2 for p in prices]</code></span></div>
  <div class="anat-row"><span>Süzme</span><span>Bazı elemanları almak: <code>[p for p in prices if p &gt; 100]</code></span></div>
  <div class="anat-row"><span>İkisi birden</span><span><code>[p * 2 for p in prices if p &gt; 100]</code></span></div>
</figure>

## Döngü yaz

- Satır bir satıra sığmıyorsa.
- Yan etki varsa: yazdırmak, dosyaya yazmak, bir şeyi güncellemek.
- İç içe ikiden fazla `for` varsa.
- Aynı turda birden fazla liste dolduruyorsan.
- Arada `break` ya da `continue` gerekiyorsa — kavramada ikisi de yok.

Son madde önemli: kavrama **her elemana bakar**. Aradığını bulunca durmak
istiyorsan döngü yazacaksın.

## Aynı iş, iki yazım

```python
prices = [80, 120, 250, 95]

# Kavrama
expensive = [price for price in prices if price > 100]

# Döngü
expensive = []
for price in prices:
    if price > 100:
        expensive.append(price)
```

İkisi de aynı sonucu veriyor. Kavrama üç satırı bire indiriyor ve
"burada yeni bir liste kuruluyor" bilgisini satırın başında veriyor.
Döngüde bunu anlamak için üç satırı da okumak gerekiyor.

## Hız

Kavrama genellikle biraz daha hızlı, çünkü `append` çağrısı her turda
yeniden aranmıyor. Fark küçük: yüz bin elemanda milisaniyeler.
**Hız için kavrama yazılmaz**, okunurluk için yazılır.

## Üç yaygın hata

1. **Yan etki için kullanmak.**

```python
[print(name) for name in names]
```

Ekrana yazıyor ama kullanılmayan bir liste de üretiyor. Döngü yaz.

2. **Süzgeci başa koymak.**

```python
[score if score >= 50 for score in scores]
```

Bu `SyntaxError`. Süzgeç sonda olur; başta olan şey `if ... else` ile
tamamlanan koşullu değerdir.

3. **Kavramanın içinde sayaç tutmak.**

```python
total = 0
[total := total + p for p in prices]
```

Çalışıyor ama okunmuyor. Toplam için `sum(prices)` var.
