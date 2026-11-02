## Kova fonksiyonu

```python
import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


def assign(user_id, salt, share_b=50):
    return "B" if bucket(user_id, salt) < share_b else "A"


print(assign("U00001", "checkout-v2"), assign("U00001", "checkout-v2"))
print(assign("U00001", "checkout-v2", share_b=10))
```

```text
B B
A
```

- Aynı kimlik + aynı tuz → her zaman aynı grup.
- `share_b` kovanın eşiği: 10 ise kullanıcıların yaklaşık %10'u B görür.
- Oranı sonradan büyütmek (10 → 50) eski B'lileri B'de tutar, yenilerini
  ekler; ama testin ortasında oran değişirse günler arasında karışım
  oluşur. Oran baştan seçilir.

## Denge tablosu

Atamadan sonra, değişiklikten etkilenemeyecek özelliklere bakılır:
platform payı, önceki ziyaret sayısı, ülke, yeni ya da eski kullanıcı.
Gruplar arasında büyük fark varsa atamada bir hata aranır.

## Yapma

- `hash()` ile atama: metinlerde her çalıştırmada değişir.
- Her deneye aynı tuzu vermek: deneyler birbirine kilitlenir.
- "İsteyen açsın" diye sunulan bir özelliği açanlarla açmayanları
  karşılaştırıp etki iddia etmek.
- Atamayı kullanıcıyla yapıp her sayfa gösterimini ayrı gözlem saymak.
