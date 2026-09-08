`WHERE` içinde kullanabileceğin karşılaştırmalar. Bu bölümde ilk dördü
yeterli; kalanlar bir sonraki bölümün konusu ama burada dursun, tek yerde
görmek işe yarıyor.

## Sayı ve metin karşılaştırma

| Operatör | Anlamı | Örnek |
|---|---|---|
| `=` | eşit | `fiyat = 450` |
| `<>` | eşit değil | `kategori <> 'Ekran'` |
| `<` | küçük | `stok < 5` |
| `>` | büyük | `fiyat > 1000` |
| `<=` | küçük veya eşit | `stok <= 0` |
| `>=` | büyük veya eşit | `fiyat >= 1000` |

`!=` de çalışıyor ve `<>` ile aynı şeyi yapıyor. Standart olan `<>`;
ekipler genelde birini seçip ona bağlı kalıyor.

## Mantıksal bağlaçlar

| Operatör | Anlamı |
|---|---|
| `AND` | iki koşul da sağlanacak |
| `OR` | en az biri sağlanacak |
| `NOT` | koşulu tersine çevirir |

**Öncelik sırası:** `NOT` → `AND` → `OR`. Yani `AND`, `OR`'dan önce
çalışıyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label"><code>==</code> yazmak</span><span class="anat-body">SQL'de yok. Eşitlik tek <code>=</code> ile.</span></div>
    <div class="anat-row"><span class="anat-label">Çift tırnak</span><span class="anat-body"><code>"Ekran"</code> metin değil, <b>nesne adı</b> demek. Metin tek tırnakla yazılıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Sayıya tırnak</span><span class="anat-body"><code>fiyat &gt; '1000'</code> çalışıyor ama sunucu her satırda dönüştürme yapıyor. Sayı sayı olarak yazılır.</span></div>
    <div class="anat-row"><span class="anat-label">Parantezsiz AND/OR</span><span class="anat-body">İkisi bir aradaysa parantez konur, doğru çalışsa bile.</span></div>
  </div>
</figure>

## Sonraki bölümde göreceklerin

Bunlar da `WHERE` içinde kullanılıyor ama ayrı bir konu:

| Operatör | Ne yapıyor |
|---|---|
| `BETWEEN` | iki değer arası (`fiyat BETWEEN 500 AND 2000`) |
| `IN` | listeden biri (`kategori IN ('Ekran', 'Aksesuar')`) |
| `LIKE` | metin deseni (`ad LIKE 'K%'`) |
| `IS NULL` | değer yok mu |

Özellikle `IN`, bu bölümdeki uzun `OR` zincirlerinin kısa yazılışı.
