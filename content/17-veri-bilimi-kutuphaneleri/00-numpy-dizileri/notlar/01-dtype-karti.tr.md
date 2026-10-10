## Tipler

| dtype | Bayt | Aralık / duyarlık |
|---|---|---|
| `int8` / `uint8` | 1 | −128…127 / 0…255 |
| `int16` | 2 | −32 768…32 767 |
| `int32` | 4 | ±2,1 milyar |
| `int64` | 8 | ±9,2 × 10¹⁸ (varsayılan tam sayı) |
| `float32` | 4 | ~7 anlamlı basamak |
| `float64` | 8 | ~16 anlamlı basamak (varsayılan ondalık) |
| `bool` | 1 | `True` / `False` |
| `<U10` | 40 | en fazla 10 karakter metin (karakter başına 4 bayt) |
| `object` | 8 + nesne | Python nesnesi; yavaş |

## Araçlar

| Yazım | Ne yapar |
|---|---|
| `a.dtype`, `a.itemsize`, `a.nbytes` | tip, eleman boyu, toplam boy |
| `np.iinfo(np.int16)` / `np.finfo(np.float32)` | sınırlar |
| `a.astype(np.int32)` | tip değiştir (yeni dizi; taşanı sessizce bozar) |
| `np.result_type(a, b)` | işlemin sonucu hangi tipte |
| `np.shares_memory(a, b)` | aynı belleği mi paylaşıyorlar? |
| `a.ravel()` / `a.flatten()` | görünüm (mümkünse) / kopya |
| `np.linspace(0, 1, 5)` | bitiş dahil eşit aralık |

## Sessiz hatalar

| Belirti | Sebep |
|---|---|
| `200` yerine `-56` | `int8` taştı |
| `300` yerine `44` | `astype(np.int8)` |
| `16777217` yerine `16777216` | `float32` duyarlığı |
| `"hello"` yerine `"hel"` | sabit genişlikli metin dizisi |
| Sayı dizisinde `<U32` | bir metin karıştı |
| `object` dtype | `None` ya da karışık nesne |
