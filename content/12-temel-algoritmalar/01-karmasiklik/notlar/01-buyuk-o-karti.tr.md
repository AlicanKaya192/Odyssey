## Sınıflar (hızlıdan yavaşa)

| Büyük O | Girdi 2 katına çıkınca iş | Tipik kod |
|---|---|---|
| `O(1)` | değişmez | indeksle erişim, formül |
| `O(log n)` | 1 adım artar | her turda yarıya bölen döngü |
| `O(n)` | 2 katına çıkar | tek döngü |
| `O(n log n)` | 2 katından biraz fazla | verimli sıralama |
| `O(n²)` | 4 katına çıkar | iç içe iki döngü |
| `O(n³)` | 8 katına çıkar | iç içe üç döngü |
| `O(2ⁿ)` | karesi alınır | bütün alt kümeleri denemek |

"Girdi iki katına çıkınca iş kaç katına çıkıyor?" sorusu, bir algoritmanın
sınıfını ölçerek bulmanın en pratik yolu.

## Sadeleştirme kuralları

- `5n + 3` → `O(n)` (sabit çarpan ve sabit terim gider)
- `n² + 100n` → `O(n²)` (küçük terim gider)
- `n + log n` → `O(n)`
- `3` → `O(1)`
- İki ayrı girdi varsa ikisi de kalır: `len(a) × len(b)` → `O(a·b)`

## Koda bakarak

```python
for x in items:          # n tur
    print(x)             # 1 adım      → O(n)

for x in items:          # n tur
    for y in items:      # her turda n → O(n²)
        ...

while n > 1:             # her turda yarıya
    n //= 2              #             → O(log n)

for x in items:          # O(n)
    ...
for x in items:          # O(n)
    for y in items:      # O(n²)
        ...              # toplam O(n + n²) = O(n²)
```

## Dikkat edilecekler

- **Gizli döngüler:** `x in liste`, `liste.index(x)`, `liste.count(x)`,
  `sum(liste)`, `max(liste)` tek satır ama her biri `O(n)`. Döngünün
  içinde kullanılırsa toplam `O(n²)` olur. (Bir sonraki bölümün konusu.)
- **Erken çıkış en kötü durumu değiştirmez:** döngüden `return` ile
  erken çıkmak en iyi durumu hızlandırır, en kötü durum yine `O(n)`.
- **Büyük O sabiti gizler:** küçük girdilerde `O(n²)` bir algoritma, sabiti
  büyük bir `O(n log n)` algoritmadan hızlı olabilir. Büyük O "büyük
  girdide ne olur" sorusunun cevabı.
