# async ve await

Bir API'nin zamanının çoğu **beklemekle** geçer: veritabanının cevabını,
başka bir API'nin cevabını, diskteki dosyayı. Bekleme sırasında işlemci
boştadır. `async` ve `await` bu boş zamanda başka isteklerle ilgilenmeyi
sağlar. FastAPI'de ikisi de var ve hangisini ne zaman yazacağını bilmek
önemli: yanlış yazılınca sunucu sessizce yavaşlıyor.

## Bir benzetme

Bir garson düşün. Mutfağa siparişi verip yemeğin pişmesini başında
**beklerse** (`time.sleep`) o sırada başka masaya bakamaz. Siparişi verip
"hazır olunca haber ver" deyip başka masaya giderse (`await`) aynı anda
birçok masaya bakabilir. `async def` "bu işlev bekleme yerlerinde başka işe
geçebilir" demek; `await` o bekleme yeri.

## İki tür uç nokta

```python
import asyncio
import time


@app.get("/async-sleep")
async def wait_well():
    await asyncio.sleep(0.5)        # beklerken başka isteklere bakılır
    return {"ok": True}


@app.get("/sync-sleep")
def wait_in_thread():
    time.sleep(0.5)                 # FastAPI bunu ayrı bir iş parçacığında çalıştırır
    return {"ok": True}
```

İkisine de **aynı anda beş istek** gönderdik (ölçtük):

```text
/async-sleep   5 istek aynı anda: 0.51 sn
/sync-sleep    5 istek aynı anda: 0.54 sn
```

İkisi de iyi: beş istek yarım saniyede bitti.

- `async def` + `await`: tek iş parçacığında, bekleme sırasında öteki
  isteklere geçerek.
- Düz `def`: FastAPI her isteği bir **iş parçacığı havuzunda** çalıştırıyor;
  biri beklerken öbürleri kendi iş parçacığında ilerliyor.

## Asıl tuzak: `async def` içinde bekletmek

```python
@app.get("/async-block")
async def wait_badly():
    time.sleep(0.5)                 # await yok!
    return {"ok": True}
```

```text
/async-block   5 istek aynı anda: 2.52 sn
```

Beş kat yavaş. `async def` işlevi FastAPI'nin **tek** olay döngüsünde
çalışıyor; `time.sleep` bekleme yeri değil, döngüyü kilitliyor. O yarım
saniye boyunca sunucu **hiçbir** isteğe bakamıyor; istekler sıraya
diziliyor. Kod doğru çalışıyor, hata vermiyor, yalnızca yavaş: bu yüzden
fark edilmesi zor.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>await asyncio.sleep(0.5)</h4><p>İstek 1 bekliyor → döngü İstek 2'ye, 3'e... geçiyor.<br>5 istek: <b>0,51 sn</b></p></div>
    <div class="no"><h4>time.sleep(0.5) (async def içinde)</h4><p>İstek 1 döngüyü kilitliyor → ötekiler sırada bekliyor.<br>5 istek: <b>2,52 sn</b></p></div>
  </div>
  <figcaption>Aynı kod, aynı sonuç, beş kat fark. <code>async def</code> içindeki bekletme bütün sunucuyu durduruyor (ölçtük).</figcaption>
</figure>

## Kural

| İşlevin içinde | Yaz |
|---|---|
| `await` ile çağrılan şeyler (`asyncio.sleep`, async kütüphaneler) | `async def` |
| Bekleten sıradan çağrılar (`time.sleep`, `sqlite3`, `requests`) | `def` |
| Yalnızca hesap, bekleme yok | İkisi de olur; `def` güvenli |

Emin değilsen `def` yaz. Yanlış `def` biraz kaynak harcar; yanlış
`async def` bütün sunucuyu kilitler.

`sqlite3` ve `requests` **bekleten** kütüphaneler: kullanıldıkları uç nokta
`def` olmalı. Önceki bölümlerdeki uç noktaların hepsi bu yüzden `def`.

## Birden fazla bekleme: sırayla mı, birlikte mi?

Bir uç noktanın iki yerden veri alması gereksin (her biri 0,3 sn):

```python
async def fetch(name, seconds):
    await asyncio.sleep(seconds)    # başka bir API'yi beklemek gibi
    return name


@app.get("/one-by-one")
async def one_by_one():
    weather = await fetch("weather", 0.3)
    news = await fetch("news", 0.3)
    return [weather, news]


@app.get("/together")
async def together():
    return await asyncio.gather(fetch("weather", 0.3), fetch("news", 0.3))
```

```text
/one-by-one  0.62 sn ['weather', 'news']
/together    0.31 sn ['weather', 'news']
```

`asyncio.gather` iki beklemeyi **aynı anda** başlatıyor; süre en uzununki
kadar. Birbirine bağlı olmayan beklemeler (birinin sonucu ötekine gerekmiyor)
böyle birleştirilir. Sonuç listesinin sırası verilen sırayla aynı.

## Cevabı beklemeden iş: `BackgroundTasks`

Kayıt olan kişiye hoş geldin e-postası göndermek zaman alır; kişinin bunu
beklemesine gerek yok. FastAPI işi cevaptan **sonraya** bırakabiliyor:

```python
from fastapi import BackgroundTasks


def send_welcome(email: str):
    time.sleep(0.5)                 # e-posta göndermek gibi yavaş bir iş
    log.append(f"welcome mail to {email}")


@app.post("/signup")
def signup(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_welcome, email)
    return {"queued": True}
```

Gerçek bir sunucuyla (uvicorn) ölçtük:

```text
POST /signup        0.03 sn  {"queued": true}
GET /log (hemen)    []
GET /log (0.7 sn)   ["welcome mail to ada@x.org"]
```

Cevap hemen gitti, iş arkadan bitti. Dikkat: `TestClient` arka plan işinin
bitmesini **bekliyor** (aynı istek testte 0,31 sn sürdü); testte iş bitmiş
olarak görünür.

Arka plan işi sunucu kapanırsa yarıda kalabilir; kaybolması kabul
edilemeyen işler (ödeme) için kullanılmaz.

## Özet

- `async def` + `await`: bekleme sırasında öteki isteklere geçer.
- Düz `def`: FastAPI iş parçacığı havuzunda çalıştırır; bekleten
  kütüphanelerle (`sqlite3`, `requests`) bu yazılır.
- `async def` içinde `time.sleep` ya da bekleten çağrı **bütün sunucuyu**
  kilitler (ölçtük: 5 kat yavaş).
- Bağımsız beklemeler `asyncio.gather` ile aynı anda.
- `BackgroundTasks`: cevaptan sonra yapılacak iş.
