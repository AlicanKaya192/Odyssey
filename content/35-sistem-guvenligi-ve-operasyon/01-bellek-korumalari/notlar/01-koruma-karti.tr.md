## Dört koruma

| Koruma | Fikir | Denetim ne zaman? |
|---|---|---|
| Yığın kanaryası | Arabellek ile dönüş bilgisi arasında rastgele değer | Fonksiyon dönmeden önce |
| DEP / NX | Veri bölgesi çalıştırılamaz (W^X) | İşlemci her komutta |
| ASLR | Adresler her çalıştırmada rastgele | Program yüklenirken |
| CFI | Atlamalar yalnızca izinli hedeflere | Her dolaylı atlamada |

## İzin dizesi

| Bölge | Olağan izin | Neden? |
|---|---|---|
| Kod | `r-x` | Çalışır ama değiştirilemez |
| Veri, öbek | `rw-` | Değişir ama çalışmaz |
| Yığın | `rw-` | Değişir ama çalışmaz |
| `rwx` | — | W^X ihlali; yalnızca zorunluysa |

## Entropi ve tahmin

| Rastgele bit | Şans | Ortalama deneme |
|---|---|---|
| 8 | 256'da 1 | 128 |
| 16 | 65 536'da 1 | 32 768 |
| 28 | 268 435 456'da 1 | 134 217 728 |

Her ek bit tahmin işini iki katına çıkarır. Ortalama deneme, olası adres
sayısının yarısıdır: `2 ** (bits - 1)`.

## Python kalıpları

- Bir bölgede W^X ihlali: `"w" in perms and "x" in perms`.
- Kanarya denetimi: `frame[size] == canary`.
- Olasılık metni: `f"1 in {2 ** bits:,}"` → `1 in 65,536`.

## Akılda tutulacak

- Kanarya **gizli** ve **rastgele** olmalı; sabit bir değer korumaz.
- Kanarya yalnızca dönüşte bakar; aynı fonksiyonda bozulan başka
  değişkeni görmez.
- Korumalar ikinci savunma hattıdır; asıl çözüm hatayı düzeltmek ya da
  bellek güvenli dil.
