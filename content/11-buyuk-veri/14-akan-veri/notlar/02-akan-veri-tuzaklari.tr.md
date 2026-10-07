Akış kodu küçük örnekte doğru çalışıp gerçek akışta yanlış sonuç verebiliyor.
Sık yapılan hatalar.

## 1. İşlenme zamanıyla pencere kurmak

Olayı geldiği ana (`time.time()`) göre pencereye koymak kolay ama yanlış:
geç gelen ödeme, olduğu dakikaya değil ulaştığı dakikaya yazılır. Pencere
**olay zamanıyla** (`event["ts"]`) kurulur.

## 2. Olayların sırayla geleceğini varsaymak

"Yeni pencerenin ilk olayı gelince öncekini kapat" kuralı sırasız akışta
olay kaybettirir (bu bölümde 6128 ödeme). Bir su işareti seçilir ve geç
kalanlar sayılır; sayı büyükse bekleme süresi artırılır.

## 3. Sonsuza kadar büyüyen durum

```python
seen.add(event["event_id"])     # her kimlik sonsuza kadar
recent[event["card"]]           # hiç silinmeyen kartlar
```

Kapanan pencereler, eski kimlikler, uzun süredir sessiz anahtarlar
temizlenmezse durum akışla birlikte büyür ve sonunda bellek biter.

## 4. Kopyaları saymak

En az bir kez teslim eden bir sistemden gelen akışta aynı olay iki kez
gelebilir; bu bölümde ciro %3 fazla çıktı. Olayın kimliğiyle ayıkla ya da
işlemi etkisiz tekrarlanabilir yap.

## 5. Her olayda yeniden uyarmak

```python
if len(times) >= 5:    # patlamanın her ödemesinde
if len(times) == 5:    # eşiğin aşıldığı anda bir kez
```

Bu bölümde `>= 5` 914, `== 5` 389 uyarı verdi. Aynı olayı bildiren uyarılar
gerçek uyarıları boğar.

## 6. Akışı listeye almak

`list(payments(...))` ya da `events.append(event)` akışı yeniden toplu
işlemeye çeviriyor ve bellek olay sayısıyla büyüyor (bu bölümde birkaç KB
yerine otuz bin KB'tan fazla). Yalnızca gereken özet tutulur.

## 7. Akışın içinde yavaş iş

Her olayda bir dosya açmak ya da ağdan bir şey sormak akışı yavaşlatır;
olaylar gelme hızından yavaş işlenirse kuyruk büyür ve gecikme sürekli artar.
Yavaş işler toplu yapılır (her 1000 olayda bir yazmak gibi).

## 8. Kafka'da sırayı her yerde beklemek

Sıra yalnızca bir bölümün içinde garanti. Sırası önemli olan olaylar (bir
kartın ödemeleri) aynı anahtarla gönderilir ki aynı bölüme düşsünler.
