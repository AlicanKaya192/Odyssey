find'ın en sık kullanılan biçimleri, bir bakışta.

## Yapı

```text
find  <nereden>  <koşullar>  <eylem>
```

Nereden: bir ya da daha fazla yol (`.` bulunduğun klasör). Koşullar: hepsi
tutmalı. Eylem: yazılmazsa yolları yazar.

## Koşullar

| Koşul | Ne seçer |
|---|---|
| `-name '*.py'` | Adı kalıba uyan (harf duyarlı) |
| `-iname '*.md'` | Aynısı, harf büyüklüğüne bakmadan |
| `-type f` | Dosyalar |
| `-type d` | Klasörler |
| `-maxdepth 1` | En fazla bu derinlik |
| `-mindepth 1` | En az bu derinlik (başlangıç klasörü dışarıda) |
| `-not -name 'k'` / `! -name 'k'` | Uymayanlar |

Gerçek terminalde ayrıca: `-size +1M`, `-mtime -7`, `-empty`, "ya da" için `-o`.

## Eylemler

| Eylem | Ne yapar |
|---|---|
| (yok) | Yolları yazar |
| `-exec komut {} \;` | Her bulunanda komutu çalıştırır |
| `-delete` | Bulunanları siler, sormadan |

## Sık kalıplar

- Bütün Python dosyaları: `find . -name '*.py'`
- Kaç tane: `find . -name '*.py' | wc -l`
- Boş klasörler dahil bütün klasörler: `find . -type d`
- İçinde kelime geçen dosyalar: `find . -name '*.py' -exec grep -l TODO {} \;`
- Yalnızca bu klasör: `find . -maxdepth 1 -type f`
