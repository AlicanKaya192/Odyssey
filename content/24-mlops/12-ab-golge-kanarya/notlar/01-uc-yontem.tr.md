Yeni model canlıya üç adımda alınır; her adım farklı bir soruyu cevaplar.

<figure class="fig">
  <div class="flow">
    <span class="node">Kapı</span>
    <span class="arrow">→</span>
    <span class="node">Gölge</span>
    <span class="arrow">→</span>
    <span class="node">Kanarya</span>
    <span class="arrow">→</span>
    <span class="node acc">A/B testi</span>
  </div>
  <figcaption>Çevrimdışı sınamadan canlı deneye.</figcaption>
</figure>

## Karşılaştırma

| | Gölge | Kanarya | A/B testi |
|---|---|---|---|
| Cevabı kim görür | Kimse | Küçük pay | Grubun yarısı |
| Etiket gerekir mi | Ayrışma için hayır | Hayır (hata, gecikme, dağılım) | Ölçüye göre |
| Bedeli | İki kat hesaplama | Yavaş yayın | Uzun süre, çok müşteri |

## Dersteki gölge ölçümü (6. ay, 1000 müşteri)

| | Eski model | Yeni model |
|---|---|---|
| Tahmin edilen iptal payı | 0,586 | 0,456 |
| Etiketlerle doğruluk | 0,685 | 0,821 |

İki model 298 müşteride farklı karar verdi.

## Kova ile yönlendirme

```python
bucket = zlib.crc32(str(customer_id).encode()) % 100
side = "new" if bucket < percent else "old"
```

- Aynı müşteri hep aynı modelde kalır.
- Pay büyüdükçe yeni modeli görmüş olanlar görmeye devam eder.

## Yapma

- Her istekte zar atarak yönlendirme; müşteri iki modelin arasında gidip
  gelir.
- Gölgenin cevabını müşteriye gösterme; gölge yalnızca kaydedilir.
