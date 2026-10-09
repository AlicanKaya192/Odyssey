# Genel Tekrar

API Yazmak modülünün sonuna geldin. API Kullanmak modülünde masanın bir tarafındaydın, istek
gönderiyordun; şimdi öbür tarafı, o istekleri karşılayan sunucuyu baştan
sona yazabiliyorsun. Bu bölümde öğrendiklerini bir isteğin yolculuğu
üzerinden bir kez daha görüyorsun; sonra 40 soruluk karışık bir sınav ve
konuları birleştiren beş alıştırma var.

## Bir isteğin yolculuğu

<figure class="fig">
  <div class="flow">
    <span class="node">Ara katman</span><span class="arrow">→</span>
    <span class="node acc">Bağımlılık<br><small>401 · 403</small></span><span class="arrow">→</span>
    <span class="node acc">Doğrulama<br><small>422</small></span><span class="arrow">→</span>
    <span class="node">Uç nokta<br><small>404 · 409</small></span><span class="arrow">→</span>
    <span class="node ok">Yanıt<br><small>201</small></span>
  </div>
  <figcaption>Her kutu bir bölüm. Bir kutuda takılan istek sonrakilere hiç ulaşmıyor; hangi kodu aldığın nerede takıldığını söylüyor.</figcaption>
</figure>

Bir `POST /books` isteği sunucuya geldiğinde sırayla şunlar oluyor:

1. **Ara katman** (15): her isteğin önünde; süre ölçmeye başlar.
2. **Yönlendirme** (01, 12): adres ve yöntem bir uç noktaya eşlenir; yoksa
   `404` / `405`.
3. **Bağımlılıklar** (09, 10): anahtar ya da jeton denetlenir (`401`,
   `403`), veritabanı bağlantısı açılır (11).
4. **Doğrulama** (02–05): yol, sorgu ve gövde kalıba ve kurallara uymalı;
   uymazsa `422` ve işlev hiç çağrılmaz.
5. **Uç nokta** (07): işini yapar; bulamazsa `404`, çakışırsa `409`
   (08).
6. **Yanıt modeli** (06): cevap süzülür (şifre çıkmaz), durum kodu konur
   (`201`).
7. Geri dönerken `yield`'li bağımlılık bağlantıyı kapatır, ara katman
   başlığı ekler, arka plan işleri (14) cevaptan sonra çalışır.

## Konular ve bölümler

| Konu | Bölüm | Ana araçlar |
|---|---|---|
| Uç nokta, yöntem | 00–01 | `@app.get`, `@app.post`, `uvicorn` |
| Yol ve sorgu | 02–03 | `{book_id}`, `limit: int = 10` |
| Gövde ve doğrulama | 04–05 | `BaseModel`, `Field`, `field_validator` |
| Cevap | 06 | `response_model`, `status_code`, `JSONResponse` |
| Tam kaynak | 07 | `POST/GET/PUT/PATCH/DELETE`, `exclude_unset` |
| Hatalar | 08 | `HTTPException`, `exception_handler` |
| Bağımlılık | 09 | `Depends`, `yield`, `dependency_overrides` |
| Kimlik | 10 | `APIKeyHeader`, `HTTPBearer`, `pbkdf2_hmac`, `secrets` |
| Veritabanı | 11 | `sqlite3`, `?`, `commit`, `rowcount` |
| Dosya düzeni | 12 | `APIRouter`, `include_router` |
| Test | 13 | `TestClient`, `pytest`, fixture |
| async | 14 | `async def`, `await`, `gather`, `BackgroundTasks`, `lifespan` |
| Belgeler | 15 | `/docs`, `summary`, CORS, ara katman |
| Model sunmak | 16 | `joblib`, Pipeline, `int()`/`float()` |

## Hangi durumda ne yaparım?

| Durum | Yap | Kod |
|---|---|---|
| Gelen değer saçma olabilir | Alana kural | `Field(ge=..., le=...)` → `422` |
| Kayıt yok | Hata fırlat | `HTTPException(404)` |
| Aynı ad zaten var | Çakışma | `409` (SQLite'ta `IntegrityError`) |
| Cevapta gizli alan var | Yanıt modeli | `response_model=UserOut` |
| Aynı kod üç uç noktada | Bağımlılık | `Depends(...)` |
| Kim olduğunu bilmiyorum | Kimlik | `401` |
| Biliyorum ama izni yok | Yetki | `403` |
| Veri kalıcı olmalı | Veritabanı | `sqlite3` + `commit` |
| Kullanıcı girdisi sorguya girecek | Parametre | `?` (asla f-string) |
| Dosya çok büyüdü | Böl | `APIRouter` |
| Değişiklik bir şeyi bozdu mu? | Test | `pytest` |
| İçeride bekleten çağrı var | Düz işlev | `def` (async değil) |
| Model bir kez yüklensin | Açılış | `lifespan` |
| Model NumPy döndürdü | Çevir | `int()`, `float()`, `.tolist()` |

## Ölçerek öğrendiğimiz tuzaklar

Patika boyunca kod çalıştırılarak bulunan, **hata vermeden** yanlış sonuç
üreten hatalar:

- `len(books) + 1` ile numara: silmeden sonra kayıt eziliyor (07).
- `PATCH`'te `exclude_unset` yok: gönderilmeyen alanlar `None`'a dönüyor
  (07); gönderilen `null` yanıt modelinde `500` yapıyor.
- Doğrulayıcıda `return` unutmak: alan `null` (05).
- `commit` unutmak: `201` ama veri yok (11).
- `async def` içinde `time.sleep`: beş kat yavaş, hata yok (14).
- Ölçekleyiciyi unutmak: her çiçeğe aynı tür (16).

Hepsinin ortak dersi: **çalışıyor görünmesi doğru olduğu anlamına gelmez.**
Testler (13) tam bunun için.

## Buradan sonra

- **Docker patikası:** bu API'yi bir imaja koymak ve her yerde aynı
  çalıştırmak.
- Notlardaki **Buradan Sonrası**: gerçek bir veritabanı (PostgreSQL),
  SQLAlchemy, JWT, sürekli entegrasyon.
