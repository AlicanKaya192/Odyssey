**Dört strateji**

| Strateji | Kesinti | Aynı anda iki sürüm | Geri dönüş hızı | Ek kaynak |
|---|---|---|---|---|
| Yeniden kur | Var | Hayır | Yavaş | Yok |
| Kademeli | Yok | Evet | Orta | Yok (kapasite düşer) |
| Mavi-yeşil | Yok | Kısa an | Anında | İki tam kopya |
| Kanarya | Yok | Evet | Hızlı | Az |

**Ne zaman hangisi?**

- Kesinti kabul edilebiliyorsa (gece bakımı, iç araç): yeniden kur.
- Çok sunucu, ek kaynak yok: kademeli.
- Anında geri dönüş şart: mavi-yeşil.
- Riskli değişiklik, çok kullanıcı: kanarya.

**Kanarya kararı**

| Durum | Karar |
|---|---|
| Yeterli istek yok | Bekle |
| Yeninin hata oranı > eskininki + izin verilen artış | Geri çek |
| Değilse | Payı artır |

```python
def decide(old, new, max_increase=0.01, min_requests=500):
    if new[1] < min_requests:
        return "wait"
    if new[0] / new[1] > old[0] / old[1] + max_increase:
        return "rollback"
    return "promote"
```

**Geri almak**

- Önceki sürümün **aynı paketini** yeniden dağıt; kodu geri alıp yeniden
  derleme.
- Paketler sürüm numarasıyla saklanır.
- Veritabanı: önce ekle (expand), sonra kaldır (contract); böylece her an
  bir önceki sürüme dönülebilir.
- Kademeli ve kanaryada iki sürüm yan yana çalışır: yeni sürüm eskinin
  anlayamayacağı bir veri biçimi yazmamalı.
