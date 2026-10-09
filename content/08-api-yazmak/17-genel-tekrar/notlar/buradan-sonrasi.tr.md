Bu patika bir API'yi baştan sona yazmayı kapsadı. Gerçek bir projeye
geçerken karşına çıkacak konular ve araçlar.

## İlk iş: kendi API'n

- Bir konu seç (kitaplığın, film listen, harcamaların) ve CRUD'unu yaz.
- SQLite'la kalıcı yap, jetonla koru, testlerini yaz.
- Docker patikasındaki yolla bir imaja koy.

## Bir sonraki adımlar

| Konu | Ne işe yarar? |
|---|---|
| PostgreSQL | Birçok kullanıcının aynı anda yazdığı gerçek veritabanı |
| SQLAlchemy / SQLModel | SQL'i Python sınıflarıyla yazmak (ORM) |
| Alembic | Tablo yapısı değişince veritabanını güncellemek (göç) |
| JWT (`PyJWT`) | Sunucunun saklamadığı imzalı jetonlar |
| `bcrypt` / `argon2` | Şifre özetinin gerçek projelerdeki hâli |
| `httpx.AsyncClient` | async uç noktadan başka API'yi çağırmak |
| GitHub Actions | Her push'ta testleri çalıştırmak (Git patikasının son notunda adı geçti) |
| Gözlem (logging, metrics) | Sunucuda ne olduğunu izlemek |

## Kaynaklar

- **FastAPI belgesi** (fastapi.tiangolo.com): öğretici ve başvuru;
  bu patikadaki her konunun ayrıntısı.
- **Pydantic belgesi** (docs.pydantic.dev): doğrulamanın bütün seçenekleri.
- **MDN HTTP** (developer.mozilla.org): durum kodları, başlıklar, CORS.

## Odyssey'de devam

- **Docker** patikası: API'yi her yerde aynı çalıştırmak.
- **API Kullanmak**: başka API'leri kullanmak; artık iki tarafı da biliyorsun.
