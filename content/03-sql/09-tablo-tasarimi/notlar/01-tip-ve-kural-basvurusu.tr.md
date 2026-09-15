Tablo kurarken elinin altında olsun diye tek sayfa. Hata metinleri bu
bölümün şemasında gerçek sunucudan alındı.

## Kalıp

```sql
CREATE TABLE tablo (
    sutun1 TIP KURALLAR,
    sutun2 TIP KURALLAR,
    CONSTRAINT kural_adi KURAL
);
```

Kurallar sütunun sonuna yazılabiliyor; birden fazla sütunu ilgilendiren
kural (birleşik anahtar, iki sütunu karşılaştıran `CHECK`) tablonun
sonuna, ayrı bir satıra.

## Tipler

| İhtiyaç | Tip | Not |
|---|---|---|
| Kimlik, adet | `INT` | |
| Para, ölçü | `DECIMAL(10,2)` | Fazla basamak **sessizce yuvarlanıyor** (`12.345` → `12.35`) |
| Metin | `NVARCHAR(n)` | Uzun metin reddediliyor, kesilmiyor |
| Tarih | `DATE` | `'2026-09-15'` biçiminde yazılıyor |

## Kurallar ve hata metinleri

| Kural | Ne zaman reddediyor | Mesaj |
|---|---|---|
| `NOT NULL` | Değer verilmezse | `Cannot insert the value NULL into column ...` |
| `PRIMARY KEY` | Aynı anahtar ikinci kez | `Violation of PRIMARY KEY constraint ...` |
| `UNIQUE` | Aynı değer ikinci kez | `Violation of UNIQUE KEY constraint ...` |
| `CHECK` | Koşul kesin yanlışsa | `... conflicted with the CHECK constraint ...` |
| `REFERENCES` | Olmayan ebeveyn | `... conflicted with the FOREIGN KEY constraint ...` |
| `REFERENCES` | Çocuğu olan ebeveyni silmek | `... conflicted with the REFERENCE constraint ...` |
| `IDENTITY` | Numarayı elle vermek | `Cannot insert explicit value for identity column ...` |

## Şaşırtan davranışlar

Hepsi ölçüldü:

- `CHECK (price > 0)` olan, boş kalabilen bir sütun `NULL`'ı **kabul
  ediyor**. Boş olmasın istiyorsan ayrıca `NOT NULL`.
- `UNIQUE` sütuna ikinci bir `NULL` **giremiyor** (SQL Server'a özgü).
- `DEFAULT` yalnızca sütun hiç yazılmazsa çalışıyor; açıkça `NULL` yazmak
  `NULL` bırakıyor.
- `IDENTITY` silinen numarayı **yeniden kullanmıyor**: 1, 3.

## Bağ seçenekleri

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">REFERENCES t(id)</span><span class="anat-body">Varsayılan: çocuğu olan ebeveyn silinemez.</span></div>
    <div class="anat-row"><span class="anat-label">ON DELETE CASCADE</span><span class="anat-body">Ebeveyn silinince çocuklar da silinir.</span></div>
    <div class="anat-row"><span class="anat-label">Boş kalabilen bağ</span><span class="anat-body"><code>NULL</code> değer hiçbir ebeveyni göstermiyor ve kabul ediliyor.</span></div>
  </div>
</figure>

## ALTER TABLE

```sql
ALTER TABLE t ADD sutun TIP NULL;                    -- eski satirlar NULL
ALTER TABLE t ADD sutun TIP NOT NULL DEFAULT deger;  -- eski satirlar deger
ALTER TABLE t DROP COLUMN sutun;
ALTER TABLE t ADD CONSTRAINT ad CHECK (kosul);
ALTER TABLE t ADD CONSTRAINT ad FOREIGN KEY (sutun) REFERENCES e(id);
```

| Deneme | Sonuç (ölçüldü) |
|---|---|
| Dolu tabloya `NOT NULL` sütun, `DEFAULT` yok | reddedildi |
| Mevcut veriye uymayan `CHECK` | reddedildi |
| Öksüz satır varken yabancı anahtar | reddedildi |
| Sütunu veriyi kesecek kadar daraltmak | reddedildi |
| Yeni sütunu aynı toplu işte kullanmak | `Invalid column name` — araya `GO` |

## Tabloyu incelemek

```sql
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'tasks'
ORDER BY ORDINAL_POSITION;
```

Bir tablonun sütunlarını, tiplerini ve boş kalıp kalamadığını gösteriyor.
`INFORMATION_SCHEMA.TABLE_CONSTRAINTS` de kurallarını listeliyor. Bu
bölümün alıştırmaları tam da böyle denetleniyor.
