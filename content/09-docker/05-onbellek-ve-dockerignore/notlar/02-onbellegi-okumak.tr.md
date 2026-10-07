"Neden her seferinde baştan kuruyor?" sorusunun cevabı derleme çıktısında.
Nasıl okunacağı ve en sık sebepler.

## Çıktıdaki işaretler

| Satır | Anlamı |
|---|---|
| `#8 CACHED` | Adım önbellekten geldi, çalıştırılmadı. |
| `#8 DONE 0.4s` | Adım çalıştırıldı ve 0,4 sn sürdü. |
| `#8 ERROR: ...` | Adım düştü; altındaki satırlar sebebi. |
| `transferring context: 140B` | Motora gönderilen bağlamın boyutu. |

Önbelleğin nerede koptuğunu bulmak için **ilk `DONE` olan adıma** bak:
ondan sonraki her şey yeniden çalışmış olmalı. Odyssey'nin terminali de
adımları `CACHED` / `DONE` olarak gösteriyor.

## Önbellek neden koptu? Kontrol listesi

1. **Kopyalanan bir dosya değişti.** `COPY . .` klasördeki herhangi bir
   dosya değişince kopuyor. Değişmesi önemsiz dosyaları (`notes.md`,
   `*.log`) `.dockerignore`'a ekle.
2. **Sıra yanlış.** `COPY . .` `pip install`'dan önceyse her kod değişikliği
   paketleri yeniden kurdurur.
3. **Talimatın metni değişti.** Bir boşluk ya da yorum dışı tek harf bile
   yeni bir adım demek.
4. **Önceki bir adım değişti.** Zincirin bir halkası koparsa sonrakilerin
   hepsi kopuyor.
5. **Taban imaj güncellendi.** `docker pull python:3.13-slim` yeni bir sürüm
   indirdiyse bütün adımlar yeniden çalışır. (Bu iyi bir şey: güvenlik
   düzeltmeleri de geliyor.)
6. **`--no-cache` verildi.**

## Önbelleği bilerek bozmak

Bazen önbellek **istenmiyor**: `RUN pip install` geçen ayki önbellekten
geliyor ve yeni bir güvenlik düzeltmesini kaçırıyorsun. Seçenekler:

- `docker build --no-cache` → hiçbir adım önbellekten gelmez (yavaş).
- `docker build --pull` → taban imajın yenisini indir, sonra derle.
- Requirements dosyasında sürümleri yükselt → zaten o adım ve sonrası
  yeniden çalışır.

## Önbellek nerede duruyor?

Önbellek Docker'ın içinde, imajlardan ayrı tutuluyor. Ne kadar yer
kapladığını `docker system df` çıktısındaki **Build Cache** satırı
gösteriyor; temizlemek için:

```text
docker builder prune
```
