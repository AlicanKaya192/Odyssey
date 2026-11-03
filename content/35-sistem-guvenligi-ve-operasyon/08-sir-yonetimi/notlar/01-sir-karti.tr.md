## Sırrın yaşam döngüsü

| Adım | Doğru yöntem | Yanlış yöntem |
|---|---|---|
| Üretmek | `secrets.token_urlsafe(32)` | `random`, kişinin uydurduğu kelime |
| Saklamak | Sır kasası, şifreli | Kodda, depoda, düz metin dosyada |
| Programa vermek | Ortam değişkeni ya da kasa | Kodun içinde sabit |
| Kullanmak | Yalnızca gereken yerde, bellekte | Kayda, hata iletisine yazmak |
| Yenilemek | Düzenli; sızınca hemen | "Çalışıyor, dokunma" |
| İptal etmek | Eski değer geçersiz kılınır | Yalnızca silmek |

## Python kalıpları

- Eksikse dur: `if not env.get(name): raise RuntimeError(...)`.
- Kayıtta gizle: `re.sub(r"(password|token)=\S+", r"\1=***", line)`.
- Son karakterleri göster: `"*" * 4 + value[-4:]`.
- Shannon entropisi: `-sum(p * math.log2(p) for p in oranlar)`.
- Yaş: `(bugun - olusturma).days > max_gun`.

## Entropi ölçeği

| Metin | Karakter başına bit |
|---|---|
| `aaaaaaaa` | 0,00 |
| `password` | 2,75 |
| `q8Zr2LxP0vT7mWk9` | 4,00 |

Tek tür karakterin tekrarı 0 bit taşır; 16 farklı karakter en çok 4 bit
taşıyabilir.

## Akılda tutulacak

- Depodan silinen sır geçmişte kalır; sızmış sayılır ve yenilenir.
- Hata iletisinde sırrın adı olur, değeri olmaz.
- Entropi taraması bir kestirimdir: yanlış alarm da verir, kaçırır da.
- `.env` gibi sır dosyaları depoya girmez ve izni `600` olur.
