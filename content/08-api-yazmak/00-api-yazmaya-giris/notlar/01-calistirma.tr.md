Kendi bilgisayarında FastAPI uygulamasını kurmak, çalıştırmak ve sık
karşılaşılan hatalar.

## Kurulum

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install fastapi uvicorn
```

Sanal ortam (Python patikasının Paketler ve Ortamlar bölümü) her projenin
paketlerini ayrı tutar. Odyssey'de bu paketler hazır; kurman gerekmez.

## Çalıştırma komutları

| Komut | Ne yapar? |
|---|---|
| `uvicorn main:app` | `main.py` içindeki `app`'i 127.0.0.1:8000'de açar. |
| `uvicorn main:app --reload` | Dosya kaydedilince yeniden başlatır (geliştirirken). |
| `uvicorn main:app --port 8001` | Başka bir port. |
| `uvicorn main:app --host 0.0.0.0` | Aynı ağdaki başka cihazlar da ulaşabilir (dikkatli kullan). |
| `Ctrl+C` | Sunucuyu durdurur. |

Adresler:

| Adres | Ne var? |
|---|---|
| `http://127.0.0.1:8000/` | Senin uç noktaların |
| `http://127.0.0.1:8000/docs` | Swagger UI: belge + "Try it out" |
| `http://127.0.0.1:8000/redoc` | ReDoc: aynı belgenin okuma görünümü |
| `http://127.0.0.1:8000/openapi.json` | Makinenin okuyacağı tarif |

## Sık hatalar (ölçüldü)

| Mesaj | Sebep | Çözüm |
|---|---|---|
| `Could not import module "mian"` | Dosya adı yanlış yazılmış ya da başka klasördesin | `main:app`'teki adı ve klasörü denetle |
| `Attribute "api" not found in module "main"` | Uygulama nesnesinin adı farklı | `app = FastAPI()` adıyla aynı yaz |
| `[Errno 10048] error while attempting to bind on address` | Port dolu (başka bir sunucu açık) | Eskisini kapat ya da `--port 8001` |
| `{"detail":"Not Found"}` | O adreste uç nokta yok | Yolu ve dekoratördeki adresi karşılaştır |
| `{"detail":"Method Not Allowed"}` | Adres var ama yöntem farklı | `@app.get` / `@app.post` |

## Kodun sonunda sunucu açmak

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
```

Böylece `python main.py` de sunucuyu açar. Odyssey bu satırı çalıştırmıyor;
denetim uygulamayı sunucusuz çağırıyor.
