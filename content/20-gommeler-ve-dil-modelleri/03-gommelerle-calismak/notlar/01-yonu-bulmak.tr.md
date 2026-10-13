Derste cinsiyet yönünü on kelime çiftinin farklarının ortalamasından kurduk.
Neden yalnızca "she − he" değil? İkisini dersteki `E`, `pairs`, `jobs` ve
`skew` ile karşılaştıralım:

```python
for name, chosen in [("she - he", [("he", "she")]), ("all pairs", pairs)]:
    g = np.mean([E[index[f]] - E[index[m]] for m, f in chosen], axis=0)
    g = g / np.linalg.norm(g)
    proj = np.array([E[index[j]] @ g for j in jobs])
    print(name, round(float(np.corrcoef(proj, skew)[0, 1]), 3))
```

```text
she - he -0.708
all pairs 0.997
```

- Tek çiftle kurulan yön önyargıyı **ters** gösteriyor (−0,708). "she" ve
  "he"nin vektörleri yalnızca cinsiyeti değil, bu iki kelimenin kendine
  özgü kullanımını da taşıyor ("she cooked", "he is a man"...). Fark
  vektörü o gürültüyü de içeriyor.
- On çiftin ortalamasında her çiftin kendine özgü gürültüsü birbirini
  götürüyor, ortak olan, yani cinsiyet, kalıyor: korelasyon 0,997.
- Bolukbasi ve arkadaşları (2016) da yönü birçok çiftin farklarından
  (PCA ile) çıkardı. Ölçtüğün yönün gerçekten ölçmek istediğin şey olduğunu
  denetle; burada verideki oranlarla karşılaştırarak yaptık.
