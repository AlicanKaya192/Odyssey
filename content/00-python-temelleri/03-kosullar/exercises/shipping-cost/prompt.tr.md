Bir kargo şirketinin ücret tablosu:

| Ağırlık | Ücret |
|---|---|
| 2 kg'a kadar (2 dahil) | 30 |
| 2 kg'dan fazla, 5 kg'a kadar (5 dahil) | 45 |
| 5 kg'dan fazla, 10 kg'a kadar (10 dahil) | 70 |
| 10 kg'dan fazla | 70 + 10'u aşan her kg için 8 |

Üyelere **%20 indirim** var, ama yalnızca ücret **50 veya fazlaysa**.

```python
weight = 10
is_member = True
```

Ücreti `cost` değişkeninde hesapla ve yazdır:

```
Cost: 56.0
```

İki adım var: önce ağırlığa göre ücreti bul, **sonra** indirimi uygula.
İndirim kararı, ilk adımda bulunan ücrete bakıyor.

> Dikkat: Sınırlar tam olarak tabloda yazdığı gibi. `10` kg ikinci değil
> üçüncü satıra, 70'e düşüyor; `<` ile `<=` arasındaki fark burada sonucu
> değiştiriyor. İndirimden sonra ücret ondalıklı çıkar.
