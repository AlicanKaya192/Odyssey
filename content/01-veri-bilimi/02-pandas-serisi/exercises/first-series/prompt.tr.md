Dört öğrencinin notunu bir seride tutacaksın — sayılarla birlikte
**adları da**.

**Yapman gerekenler:**

1. pandas'ı `pd` adıyla al.
2. `[82, 74, 91, 68]` notlarını `["Ada", "Kerem", "Mina", "Deniz"]`
   etiketleriyle bir seride tut, adı `scores` olsun.
3. Sırayla yazdır: serinin kendisi, Mina'nın notu, ortalama (iki basamağa
   yuvarlanmış), ve **en yüksek notu alanın adı**.

**Beklenen çıktı:**

```
Ada      82
Kerem    74
Mina     91
Deniz    68
dtype: int64
91
78.75
Mina
```

**İpucu:** son satır için `idxmax()` var. NumPy'da `argmax` sırayı
veriyordu; pandas'ta `idxmax` doğrudan **etiketi** veriyor — index'in ne işe
yaradığı burada görünüyor.
