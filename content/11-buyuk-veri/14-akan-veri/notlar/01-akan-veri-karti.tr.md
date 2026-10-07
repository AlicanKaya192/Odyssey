Akan verinin kavramları ve bu bölümdeki kalıplar tek sayfada.

## Kavramlar

| Kavram | Anlamı |
|---|---|
| Olay | Akıştaki tek kayıt: kimlik, zaman, veri |
| Durum | Akış boyunca güncellenen küçük özet |
| Olay zamanı | Olayın olduğu an |
| İşlenme zamanı | Olayın sisteme ulaştığı an |
| Su işareti | "Bundan eskisi artık gelmez" varsayımı |
| Etkisiz tekrar | Aynı olayı iki kez işlemek bir kezle aynı |

## Pencereler

| Pencere | Nasıl | Örnek soru |
|---|---|---|
| Sabit | Örtüşmeyen eşit dilimler | Her dakikada kaç ödeme? |
| Kayan | Son N saniye, her olayla kayar | Kart son 60 sn'de 5 ödeme yaptı mı? |
| Oturum | Boşluk süresini aşınca kapanır | Bir ziyarette kaç sayfa? |

## Kalıplar

```python
# Sabit pencerenin başlangıcı
start = event["ts"] // 60 * 60

# Kayan pencere (kart başına)
times = recent[event["card"]]
times.append(event["ts"])
while times[0] <= event["ts"] - 60:
    times.popleft()

# Su işareti
watermark = newest - lateness
if start + 60 <= watermark:
    ...  # geç kaldı: at ya da ayrıca kaydet

# Kopyaları ayıklamak
if event["event_id"] in seen:
    continue
seen.add(event["event_id"])
```

## Teslim garantileri

| Garanti | Olay | Bedeli |
|---|---|---|
| En fazla bir kez | Kaybolabilir | Eksik sonuç |
| En az bir kez | İki kez gelebilir | Kopya ayıklamak gerekir |
| Tam bir kez | Bir kez sayılır | Sistem desteği, daha yavaş |

## Kafka terimleri

| Terim | Anlamı |
|---|---|
| Üretici | Konuya kayıt yazan program |
| Konu | Bir olay türünün akışı |
| Bölüm | Konunun parçası; yalnızca sonuna eklenir |
| Ofset | Kaydın bölümdeki sırası |
| Anahtar | Bölümü belirler; aynı anahtar aynı bölüm |
| Onaylama | Tüketicinin nerede kaldığını kaydetmesi |
| Tüketici grubu | Bölümleri paylaşan tüketiciler |
| Saklama süresi | Kayıtların silinmeden durduğu süre |

## Araçlar

| Araç | Yer |
|---|---|
| Kafka, Kinesis, Pub/Sub | Taşıma ve saklama |
| Spark Structured Streaming | Küçük toplu işlerle akış |
| Flink | Olay olay, düşük gecikme |
