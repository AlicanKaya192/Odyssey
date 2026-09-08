SSMS alıştırmalar için gerekmiyor, ama sahada SQL yazan herkesin ekranında
açık duruyor. Bu not kısa bir tur: pencerede ne nerede.

## Bağlanmak

Program açılınca ilk çıkan pencere bağlantı penceresi:

| Kutu | Ne yazılacak |
|---|---|
| Server type | `Database Engine` |
| Server name | `.\SQLEXPRESS` |
| Authentication | `Windows Authentication` |
| Encryption | `Optional` |

**Connect**'e bastıktan sonra pencere kapanıyor ve solda bir ağaç
beliriyor. Bağlanmış oldun.

## Soldaki ağaç: Object Explorer

Sunucunun içindekiler burada duruyor. Açılış hâli şöyle:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Databases</span><span class="anat-body">Sunucudaki veritabanları. Odyssey'in alıştırma veritabanlarını (<code>Odyssey_</code> önekli) burada göreceksin.</span></div>
    <div class="anat-row"><span class="anat-label">System Databases</span><span class="anat-body">SQL Server'ın kendi işleri için kullandığı dört veritabanı: <code>master</code>, <code>model</code>, <code>msdb</code>, <code>tempdb</code>. Bunlara dokunmuyoruz.</span></div>
    <div class="anat-row"><span class="anat-label">Security</span><span class="anat-body">Kullanıcılar ve yetkiler.</span></div>
    <div class="anat-row"><span class="anat-label">Server Objects</span><span class="anat-body">Yedekleme hedefleri, bağlı sunucular. İleri seviye konular.</span></div>
  </div>
</figure>

Bir veritabanını açtığında altında **Tables** görüyorsun; onu da açınca
tablolar sıralanıyor. Bir tablonun altındaki **Columns** sütunları ve
tiplerini gösteriyor — bir tablonun neye benzediğini anlamanın en hızlı
yolu bu.

## Tabloya bakmak

Bir tabloya sağ tıklayıp **Select Top 1000 Rows** dersen SSMS senin yerine
sorguyu yazıyor ve sonucu gösteriyor. İlk günlerde tabloyu tanımak için
çok işe yarıyor.

## Sorgu yazmak

Üstteki **New Query** düğmesi boş bir sorgu sekmesi açıyor.

Yazdıktan sonra **F5** çalıştırıyor. Metnin bir kısmını seçip F5'e
basarsan **yalnızca seçili kısım** çalışıyor — uzun bir dosyanın içinden
tek sorgu denemenin yolu bu.

Sekmenin hangi veritabanına bağlı olduğu üstteki açılır kutuda yazıyor.
Yanlış veritabanındayken "böyle bir tablo yok" hatası alıyorsun; ilk
bakılacak yer orası.

## `GO` nedir?

SSMS'te yazılan betiklerde satır başına `GO` görürsün. Bu **SQL değil**;
SSMS'in "buraya kadar olanı gönder" komutu. Sunucu `GO` diye bir şey
bilmiyor.

Odyssey de `GO` satırlarını aynı şekilde anlıyor, yani SSMS'ten
kopyaladığın bir betik olduğu gibi çalışıyor.

## Kısayollar

| Tuş | Ne yapar |
|---|---|
| `F5` | Çalıştırır |
| `Ctrl + N` | Yeni sorgu sekmesi |
| `Ctrl + Shift + R` | Tamamlama listesini tazeler (yeni tablo görünmüyorsa) |
| `Ctrl + K, Ctrl + C` | Seçili satırları yorum yapar |
| `Ctrl + K, Ctrl + U` | Yorumu kaldırır |
