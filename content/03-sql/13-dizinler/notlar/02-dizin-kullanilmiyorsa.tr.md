Bir dizin kurdun, sorgu hâlâ yavaş. Bu bölümde ölçülen durumlarda sebep
hep şu altısından biriydi. Hiçbiri hata vermiyor — sorgu doğru sonucu
getiriyor, yalnızca tabloyu baştan sona okuyarak.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">İşlev</span><span class="anat-body">Sütun bir işlevin içinde: <code>YEAR(created_at)</code>, <code>UPPER(session_code)</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Baştaki %</span><span class="anat-body"><code>LIKE '%0050'</code> sıralı listede aranamıyor.</span></div>
    <div class="anat-row"><span class="anat-label">İlk sütun yok</span><span class="anat-body">Bileşik dizinin ilk sütunu <code>WHERE</code>'de geçmiyor.</span></div>
    <div class="anat-row"><span class="anat-label">Fazla geri dönüş</span><span class="anat-body">İstenen sütunlar dizinde yok ve satır sayısı büyük.</span></div>
    <div class="anat-row"><span class="anat-label">Düşük seçicilik</span><span class="anat-body">Aranan değer tablonun büyük bir parçası.</span></div>
    <div class="anat-row"><span class="anat-label">Süzgeç uymuyor</span><span class="anat-body">Aranan satırlar süzgeçli dizinde yok.</span></div>
  </div>
</figure>

## 1. İşlev

| `WHERE` | Okuma |
|---|---|
| `created_at >= '2025-06-01' AND created_at < '2025-06-02'` | 2 |
| `YEAR(created_at) = 2025 AND MONTH(...) = 6 AND DAY(...) = 1` | 42 |
| `DATEADD(day, 1, created_at) >= ...` | 42 |
| `UPPER(session_code) = 'S010000'` | 54 |

**Çare:** işlevi sütundan alıp karşı tarafa yaz. `YEAR = 2025` yerine
`>= '2025-01-01' AND < '2026-01-01'`. Harf büyüklüğü için bu sunucuda
zaten gerek yok: karşılaştırmalar büyük/küçük harfe duyarsız (onuncu
bölüm).

`CAST(created_at AS DATE) = '2025-06-01'` bir istisna: 2 okumayla aradı.
İstisnaya güvenmek yerine kurala uymak daha az sürpriz çıkarır.

## 2. Baştaki %

`LIKE 'S0050%'` 3 okuma, `LIKE '%0050'` 54. Başı belli olmayan bir metin
sıralı bir listede aranamıyor.

**Çare:** mümkünse aramayı başından yap. Sondan arama gerçekten
gerekiyorsa bu bölümün konusu olmayan başka araçlar var (tam metin
araması gibi).

## 3. Bileşik dizinde ilk sütun yok

`(customer_id, created_at)` dizini varken yalnızca `created_at` ile arama
52 okuma — dizinin tamamı. Aynı dizinle yalnızca `customer_id` ile arama
11 okuma.

**Çare:** dizini sorguya göre kur. Hangi sütun tek başına da aranıyorsa
o önde olmalı.

## 4. Fazla geri dönüş

`created_at` dizini varken bir günün 58 satırı için `SELECT *` tabloyu
taradı (150 okuma), 15 satırlık bir sorgu dizini kullanıp her satır için
tabloya döndü (130 okuma). Sunucu, geri dönüş sayısı büyüyünce taramayı
seçiyor.

**Çare:** `SELECT *` yerine gereken sütunları yaz; sık çalışan bir sorgu
için gereken sütunları `INCLUDE` ile dizine ekle (150 → 3).

## 5. Düşük seçicilik

`event_type` dört değer alıyor. `'purchase'` 5 000 satır: `SELECT id` 22
okumayla dizinden geldi, `SELECT *` tabloyu taradı.

**Çare:** dizini çok satırı eleyen sütunlara kur. Tek başına az değer
alan bir sütun, bileşik bir dizinin ikinci sütunu olarak daha çok işe
yarar.

## 6. Süzgeç uymuyor

`WHERE amount IS NOT NULL` süzgeçli dizinle `amount > 490` 2 okuma;
`amount IS NULL` 150 — o satırlar dizinde yok.

**Çare:** süzgeçli dizini, sorguların hep aradığı parça için kur.

## Bir de: dizin sayısı

Her dizin yazmayı pahalılaştırıyor: tek satırlık `INSERT` 2 okumadan, beş
dizinle 22'ye çıktı. Kullanılmayan bir dizin yalnızca bedel.

## Kontrol soruları

Bir sorgu yavaşsa sırayla sor:

- **Sütun çıplak mı?** `WHERE`'de sütunun kendisi mi var, bir işlevin
  sonucu mu?
- **Dizinin ilk sütunu sorguda geçiyor mu?**
- **Kaç satır dönüyor ve istenen sütunlar dizinde mi?**
