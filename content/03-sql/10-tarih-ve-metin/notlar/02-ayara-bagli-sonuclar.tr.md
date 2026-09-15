Aynı sorgu iki farklı sunucuda iki farklı sonuç verebiliyor. Hata da
vermiyor; yalnızca sonuç değişiyor. Bu not, bu bölümde ölçülen ayara
bağlı davranışları ve her birinin nasıl sabitleneceğini topluyor.

## Hangi ayarlar

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Dil ayarı (collation)</span><span class="anat-body">Harflerin nasıl karşılaştırıldığı ve büyütülüp küçültüldüğü. Bu makinede <code>Turkish_CI_AS</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Oturum dili</span><span class="anat-body">Ay ve gün adlarının hangi dilde yazıldığı. Bu makinede <code>us_english</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Tarih biçimi</span><span class="anat-body"><code>'03/04/2026'</code> gibi bir metnin gün mü ay mı diye okunduğu (<code>SET DATEFORMAT</code>).</span></div>
    <div class="anat-row"><span class="anat-label">Haftanın ilk günü</span><span class="anat-body"><code>DATEPART(weekday, ...)</code>'in kaç döndürdüğü. Bu makinede <code>@@DATEFIRST = 7</code> (Pazar).</span></div>
  </div>
</figure>

Hepsi kurulumda ya da oturumda seçiliyor; senin sunucun farklı olabilir.

## 1. Tarih metni

| Yazım | Ayar | Okunan gün |
|---|---|---|
| `'03/04/2026'` | `dmy` | 3 Nisan |
| `'03/04/2026'` | `mdy` | 4 Mart |
| `'2026-03-04'` → `DATETIME` | `dmy` | **3 Nisan** |
| `'2026-03-04'` → `DATE` | `dmy` | 4 Mart |
| `'20260304'` | her ayar | 4 Mart |

**Sabitlemek:** `DATE` için `'YYYY-MM-DD'`, `DATETIME` için
`'YYYYMMDD'`. Eğik çizgili yazım hiç kullanılmıyor.

## 2. Ay ve gün adları

`DATENAME(month, '2026-03-14')` bu sunucuda `March` verdi,
`DATENAME(weekday, ...)` da `Saturday`. Türkçe oturumda aynı sorgu `Mart`
ve `Cumartesi` verir.

**Sabitlemek:** kültürü açıkça ver.

```sql
FORMAT(d, 'MMMM yyyy', 'tr-TR')   -- Mart 2026
FORMAT(d, 'MMMM yyyy', 'en-US')   -- March 2026
```

## 3. Haftanın günü numarası

`DATEPART(weekday, '2026-03-14')` bu sunucuda **7** verdi: hafta Pazar
başladığı için Cumartesi yedinci gün. `SET DATEFIRST 1` ile haftayı
Pazartesi başlatınca aynı gün **6** oldu.

Bu ayar oturum diliyle birlikte de değişiyor: `SET LANGUAGE Turkish`
yazıldıktan sonra `@@DATEFIRST` kendiliğinden 1 oldu. Yani sorgunun
kendisine dokunmadan, yalnızca oturum dilini değiştirmek hafta sonu
süzen bir sorgunun sonucunu değiştiriyor.

**Sabitlemek:** gün numarasıyla karar veren bir sorguda (hafta sonu
süzmek gibi) ayara güvenme; ya `SET DATEFIRST 1` ile ayarı sorgunun
başında kendin koy ya da `DATENAME` yerine tarih aralığıyla çalış.

## 4. Türkçe I

| İfade | Türkçe ayar | Latin ayar |
|---|---|---|
| `UPPER('istanbul')` | `İSTANBUL` | `ISTANBUL` |
| `LOWER('ISTANBUL')` | `ıstanbul` | `istanbul` |
| `WHERE city = 'istanbul'` | **0 satır** | 2 satır |
| `WHERE city LIKE 'ist%'` | **0 satır** | 2 satır |

Türkçede `I`'nın küçüğü `ı`, `i`'nin büyüğü `İ`. Türkçe ayarlı sunucu buna
uyuyor ve `Istanbul` yazan bir kaydı `istanbul` araması bulamıyor.

**Sabitlemek:** karşılaştırmada dil ayarını açıkça söyle.

```sql
WHERE city COLLATE Latin1_General_CI_AS = 'istanbul'   -- 2 satir
```

## 5. Büyük/küçük harf ve anahtarlar

Bu sunucuda karşılaştırmalar harf büyüklüğüne duyarsız (`CI`): önceki
bölümde `w1` ile `W1` aynı birincil anahtar sayıldı. Büyük/küçük harfi
ayıran (`CS`) bir sunucuda ikisi ayrı olurdu.

## Bu uygulamanın alıştırmaları

Beklenen sonuçlar Türkçe ayarlı bir sunucuda üretildi, ama her SQL
alıştırması **Latin ayarlı bir veritabanında da** çalıştırıldı ve hepsi
aynı sonucu verdi. Yani alıştırmaları hangi dilde kurulmuş bir sunucuda
çözersen çöz, doğru çözüm geçiyor.

## Kontrol sorusu

Bir sorgu yazdığında kendine sor: **"Bu sonuç sunucunun diline, tarih
biçimine ya da hafta ayarına bağlı mı?"** Cevap evetse ayarı sorgunun
içinde açıkça söyle.
