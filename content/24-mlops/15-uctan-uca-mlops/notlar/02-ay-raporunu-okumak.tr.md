Hattın her ay yazdığı satır bir karardır; her kararın bir sonraki adımı var.

## Dersteki sekiz ay

| Ay | Kayma | Doğruluk | Karar |
|---|---|---|---|
| 1 | 0,070 | 0,813 | keep |
| 3 | 0,578 | 0,778 | v2 promoted (0,782) |
| 4 | 0,326 | 0,787 | candidate kept out (0,784) |
| 5 | 0,575 | 0,691 | data rejected (100% invalid) |
| 6 | 0,922 | 0,697 | v3 promoted (0,837) |
| 7 | 0,127 | 0,821 | keep |

## Her karardan sonra

| Karar | Ne yapılır |
|---|---|
| `keep` | Hiçbir şey; izlemeye devam |
| `promoted` | Yeni sürüm gölge ve kanaryadan geçirilir; eski sürüm geri dönüş için kayıtta kalır |
| `kept out` | Adayın ölçümü kayda girer; kayma sürüyorsa pencere boyu yeniden düşünülür |
| `data rejected` | Uyarı; veri kaynağı düzeltilir, hat elle yeniden çalıştırılır |

## Bozuk veri kapıdan geçebilir mi?

| Aday nerede ölçüldü | Doğruluk |
|---|---|
| Aynı bozuk kaynaktan gelen kümede | 0,784 |
| Kaynak düzeldikten sonra temiz veride | 0,673 |

Kapının kümesi de bozuksa aday kapıdan geçer; doğrulama bu yüzden kapıdan
önce gelir.

## Yapma

- `data rejected` satırını sessiz bırakma; model bir ay daha eski kalır.
- `kept out` satırını hata sanma; kapı işini yaptı.
