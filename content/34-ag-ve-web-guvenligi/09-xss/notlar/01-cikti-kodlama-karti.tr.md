## HTML kodlama tablosu

| Karakter | Kodlanmış hâli |
|---|---|
| `&` | `&amp;` (ilk önce) |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |

Python: `html.escape(text)` beşini de kodlar (`quote=True` varsayılan).

## Bağlama göre

| Nereye gidiyor? | Ne yapılır? |
|---|---|
| HTML gövdesi | `html.escape` |
| Öznitelik değeri | `html.escape`, değer her zaman tırnak içinde |
| Bağlantı (`href`, `src`) | Şema izin listesi (`http`, `https`) + `html.escape` |
| `<script>` bloğunun içi | Kullanıcı verisi yazılmaz |
| Adres parametresi | `urllib.parse.quote` (URL kodlama) |

## Savunma katmanları

1. **Çıktı kodlama** (bağlama uygun): asıl savunma.
2. **Otomatik kodlayan şablon:** unutmayı önler; "ham/güvenli" işaretleri
   dikkatle.
3. **CSP:** `script-src 'self'`; `'unsafe-inline'` yok.
4. **`HttpOnly` çerez:** sızan betik çerezi okuyamaz.
5. **Girdi doğrulama:** beklenen tür ve biçim.

## XSS türleri

| Tür | Metin nereden gelir? |
|---|---|
| Kalıcı | Veritabanı (yorum, profil) |
| Yansıtılan | Aynı istek (arama kutusu, parametre) |
| DOM tabanlı | Sayfanın kendi JavaScript'i |

## Kurallar

- Kodlama veriyi **yazarken** yapılır, kaydederken değil: aynı veri HTML'e,
  JSON'a, e-postaya farklı kodlamayla gider.
- Biçimli metin gerekiyorsa kendi süzgecini yazma; izin listeli, bakımı
  süren bir temizleme kütüphanesi kullan.
- Bir değerin "zaten temiz" olduğunu varsayma; şablon kodlasın.
