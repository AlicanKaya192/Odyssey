Bu patika bir sipariş veritabanında SQL Server'ın sorgu dilini baştan
sona gezdi. Aşağısı, "şimdi ne yapmalıyım" sorusunun sırayla cevabı.

## Önce: kendi veritabanın

Ders verisinde çalışan bir şey henüz senin değil.

- Bildiğin bir alan seç: kitaplığın, bir oyunun skorları, bir kulübün
  üyeleri, harcamaların.
- **Tabloları kendin tasarla.** Hangi bilgi hangi tabloda, neyin
  birincil anahtarı ne, hangi sütun hangi tabloya bağlı — bu patikada şema
  hazır geldi; gerçek hayatta en zor karar bu.
- Kuralları baştan koy: `NOT NULL`, `CHECK`, `FOREIGN KEY`. Bu patikanın
  şemasında yabancı anahtar yoktu ve bir müşteri silinince siparişleri
  öksüz kaldı.
- Sonra kendine on soru yaz ve her birini tek sorguyla cevapla.

**Öğrendiğinin sınavı şu:** bir sorgunun sonucunu görmeden kaç satır
döneceğini tahmin edebiliyor musun?

## Başka veritabanı sistemleri

SQL'in çekirdeği — `SELECT`, `JOIN`, `GROUP BY`, pencereler, `WITH` —
hemen her sistemde aynı. Farklar lehçede. Bu patikada gördüğün bazı
şeyler T-SQL'e özgü: `TOP`, `GETDATE()`, `ISNULL`, `IDENTITY`, metni `+`
ile birleştirmek, `THROW`. PostgreSQL, MySQL ya da SQLite'a geçtiğinde bu
birkaç şeyin karşılığını aramak yetiyor; örneğin satır sınırlamak
oralarda `TOP` yerine `LIMIT` ile yazılıyor.

Bu yüzden patika boyunca taşınabilir yazımları seçtik: `COALESCE`
(`ISNULL` yerine), `CASE`, yarı açık tarih aralığı.

## Python'dan SQL

Bu uygulama sorgularını Python'dan `pyodbc` ile gönderiyor. Aynı yol
senin programların için de açık:

- `pyodbc` ya da `sqlalchemy` ile bağlan, sorguyu çalıştır, satırları al.
- Veri Bilimi patikasındaki `pandas`, bir sorgunun sonucunu doğrudan bir
  DataFrame'e okuyabiliyor (`pandas.read_sql`).
- **Kullanıcıdan gelen değeri sorguya metin olarak yapıştırma;**
  parametre kullan (`WHERE id = ?`). Metin yapıştırmak "SQL enjeksiyonu"
  denen güvenlik açığının kaynağı.

## Yürütme planı

Dizinler bölümünde okuma sayısını ölçtün. SQL Server Management Studio
bir sorgunun **planını** — hangi dizini kullandığını, nerede tarama
yaptığını — çizerek gösteriyor. Yavaş bir sorguda ilk bakılacak yer
orası.

## İşlemler ve eşzamanlılık

Bu patikada her şey tek başına çalıştı. Gerçek bir veritabanında aynı
anda birçok kişi yazıyor. Sıradaki konular: işlemin tam anlamı
(`BEGIN TRAN`, `COMMIT`, `ROLLBACK`), kilitler ve yalıtım düzeyleri, iki
kişinin aynı satırı değiştirmeye çalışması.

## Tasarım

Tablo tasarımı bölümü kuralları gösterdi. Bir sonraki adım **normal
biçimler**: aynı bilginin iki yerde tutulmaması, tabloların neden
bölündüğü. Rapor ve analiz için kurulan veritabanlarında ise tersine bir
yaklaşım var: yıldız şeması.

## Bu uygulamada

Veri Bilimi patikası SQL'in çektiği veriyle ne yapılacağını anlatıyor;
Makine Öğrenmesi patikası o veriden model kurmayı. SQL, ikisinin de
başındaki adım.
