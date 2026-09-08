`LIKE`, `IN` ve `BETWEEN` için tek sayfalık başvuru.

## LIKE desenleri

| Desen | Eşleşir | Eşleşmez |
|---|---|---|
| `'K%'` | Klavye, Kablo, K | Fare |
| `'%uk'` | Kucuk, uk | ukulele |
| `'%la%'` | Klavye, lamba, la | Fare |
| `'F_re'` | Fare, Fire | Fre, Faare |
| `'____'` | tam dört karakterli her şey | üç ya da beş karakterli |

`%` sıfır karakterle de eşleşiyor: `'K%'` deseni tek harflik `K` metnini
de buluyor.

## Köşeli parantez: SQL Server'a özgü

T-SQL'de bir de karakter kümesi var. Standart SQL'de yok, başka
veritabanlarına taşınmıyor.

| Desen | Anlamı |
|---|---|
| `'[KM]%'` | K ya da M ile başlayan |
| `'[A-F]%'` | A ile F arası bir harfle başlayan |
| `'[^K]%'` | K ile başlamayan |

## Jokerin kendisini aramak

```sql
WHERE aciklama LIKE '%50!%%' ESCAPE '!'
```

`ESCAPE` ile seçtiğin karakter, kendisinden sonra geleni **düz metin**
yapıyor. `!%` gerçek yüzde işareti; sondaki `%` hâlâ joker.

Kaçış karakterini sen seçiyorsun; metinde geçmeyen bir şey olması yeterli.

## Hız notu

| Desen | İndeks kullanılabilir mi |
|---|---|
| `'K%'` | **evet** — başı belli |
| `'%K'` | hayır |
| `'%K%'` | hayır |

Baştaki `%`, sunucunun nereden başlayacağını bilememesi demek; her satıra
tek tek bakması gerekiyor. Küçük tablolarda fark edilmiyor, büyük
tablolarda en sık karşılaşılan yavaşlık sebeplerinden.

## IN

```sql
WHERE kategori IN ('Ekran', 'Yazilim')
```

Şununla birebir aynı:

```sql
WHERE kategori = 'Ekran' OR kategori = 'Yazilim'
```

- Liste **boş olamaz**: `IN ()` sözdizimi hatası.
- Liste bir **alt sorgu** da olabilir: `IN (SELECT kod FROM tedarikciler)`.
  Bu, alt sorgular bölümünün konusu.
- `NOT IN` ile `NULL` bir arada **her zaman boş sonuç** veriyor; ayrıntısı
  NULL notunda.

## BETWEEN

```sql
WHERE fiyat BETWEEN 500 AND 3000
```

Şununla birebir aynı:

```sql
WHERE fiyat >= 500 AND fiyat <= 3000
```

- **İki uç da dahil.** Dışarıda bırakmak istiyorsan `BETWEEN` kullanma.
- **Küçük değer önce.** `BETWEEN 3000 AND 500` hata vermiyor, boş sonuç
  veriyor.
- Tarihlerde de çalışıyor ama dikkat gerekiyor: `BETWEEN '2026-01-01' AND
  '2026-01-31'` yazarsan 31 Ocak saat 00:00'dan **sonrası** dışarıda
  kalıyor. Tarih-saat sütunlarında `>= baslangic AND < bitis` daha
  güvenli.

## Hangisini ne zaman

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Belirli değerler</span><span class="anat-body"><code>IN</code> — üç kategori, beş şehir, iki durum kodu</span></div>
    <div class="anat-row"><span class="anat-label">Sayı ya da tarih aralığı</span><span class="anat-body"><code>BETWEEN</code>, ya da sınır dışarıda kalacaksa <code>&gt;=</code> ve <code>&lt;</code></span></div>
    <div class="anat-row"><span class="anat-label">Metin parçası</span><span class="anat-body"><code>LIKE</code></span></div>
    <div class="anat-row"><span class="anat-label">Değer var mı yok mu</span><span class="anat-body"><code>IS NULL</code> / <code>IS NOT NULL</code></span></div>
  </div>
</figure>
