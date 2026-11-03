# SQL Enjeksiyonu

OWASP Top 10 bölümünde enjeksiyonun özünü tek cümleyle söyledik:
**kullanıcının verisi, kodun bir parçası gibi yorumlanıyor.** Orada adında
kesme işareti olan bir kişinin sorguyu kazara bozduğunu gördük. Bu bölüm
aynı açığın neden bu kadar tehlikeli olduğunu, kalıcı çözümün neden
**parametreli sorgu** olduğunu ve parametrenin yetmediği üç yeri
anlatıyor. Bütün örnekler Python'ın `sqlite3` modülüyle **bellekte**
kurulan küçük tablolarda çalışıyor; dışarıdaki hiçbir veritabanına
dokunulmuyor.

## Sorgu metinle kurulunca

Bir uygulama kullanıcının siparişlerini göstermek istiyor. Sorguyu
f-string ile kuruyor:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INTEGER, owner TEXT, item TEXT)")
conn.executemany("INSERT INTO orders VALUES (?, ?, ?)",
                 [(1, "ada", "book"), (2, "ada", "pen"),
                  (3, "bob", "laptop"), (4, "eve", "phone")])


def orders_bad(owner):
    query = f"SELECT item FROM orders WHERE owner = '{owner}'"
    return conn.execute(query).fetchall()


owner = "x' OR '1'='1"
print(orders_bad("ada"))
print(f"SELECT item FROM orders WHERE owner = '{owner}'")
print(len(orders_bad(owner)))
```

```text
[('book',), ('pen',)]
SELECT item FROM orders WHERE owner = 'x' OR '1'='1'
4
```

Normal bir adla doğru çalışıyor. Ama girdinin içindeki `'` işareti metni
erken kapatıyor ve geri kalanı (`OR '1'='1'`) SQL olarak okunuyor. Ortaya
çıkan sorgunun koşulu artık her satır için doğru: başkalarının dahil
bütün siparişler (4 satır) geldi. Saldırgan veriyi değil, **sorgunun
anlamını** değiştirdi. Aynı yolla bir giriş formunda parola denetimi
atlanabilir ya da başka tablolardaki veri okunabilir; açığın ne kadar
ileri götürülebileceği uygulamaya bağlıdır, ama kök neden hep aynıdır.

## Kalıcı çözüm: parametreli sorgu

Veriyi metne yapıştırmak yerine sorgu ile veriyi **ayrı** göndeririz. Sorgu
metninde verinin yerine bir yer tutucu (`?`) durur; veritabanı önce
sorguyu ayrıştırır, sonra gelen değeri **her zaman veri olarak** yerine
koyar:

```python
def orders(owner):
    return conn.execute("SELECT item FROM orders WHERE owner = ?",
                        (owner,)).fetchall()


print(orders("ada"))
print(len(orders("x' OR '1'='1")))
```

```text
[('book',), ('pen',)]
0
```

Aynı girdi şimdi yalnızca "adı `x' OR '1'='1` olan sahip" olarak arandı ve
hiçbir satır gelmedi. Değerin içinde ne olduğunun önemi kalmadı: tırnak,
noktalı virgül, SQL kelimesi, hepsi metnin parçası. Bu yüzden parametreli
sorgu "tehlikeli karakterleri ayıklamaktan" çok daha sağlamdır; ayıklama
listesi bir şeyi hep unutur, parametre ise hiçbir şeyi koda çevirmez.

<figure class="fig"><div class="versus">
  <div class="no"><h4>Metin birleştirme</h4><code>"... WHERE owner = '" + owner + "'"</code><br>Veri sorgu metnine yapıştırılır; içindeki işaretler SQL olarak okunabilir.</div>
  <div class="ok"><h4>Parametreli sorgu</h4><code>"... WHERE owner = ?", (owner,)</code><br>Sorgu ve veri ayrı gider; veri hiçbir zaman kod olmaz.</div>
</div><figcaption>f-string, <code>+</code>, <code>%</code> ve <code>.format</code> ile kurulan sorguların hepsi soldaki gruptadır.</figcaption></figure>

Dikkat: `(owner,)` tek elemanlı bir **demettir**; virgül unutulursa
Python onu düz metin sanar. Yer tutucunun biçimi kütüphaneye göre
değişebilir (`?`, `%s`, `:name`), ama fikir hep aynıdır. ORM
kütüphaneleri de arkada parametre kullanır; onların içinde ham sorguyu
metinle kurmak aynı açığı geri getirir.

## Parametrenin yetmediği yer 1: sütun ve tablo adları

Yer tutucu yalnızca **değerlerin** yerine geçer; sütun ya da tablo adının
yerine geçemez. Kullanıcı "fiyata göre sırala" seçince sütun adını
parametreyle vermeyi denemek sessizce yanlış çalışır:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (name TEXT, price INTEGER)")
conn.executemany("INSERT INTO products VALUES (?, ?)",
                 [("pen", 3), ("book", 12), ("bag", 30), ("cup", 7)])

print(conn.execute("SELECT name FROM products ORDER BY ?", ("price",)).fetchall())

SORTABLE = {"name": "name", "price": "price"}


def products(sort):
    column = SORTABLE.get(sort, "name")
    return [r[0] for r in conn.execute(f"SELECT name FROM products ORDER BY {column}")]


print(products("price"))
print(products("rating"))
```

```text
[('pen',), ('book',), ('bag',), ('cup',)]
['pen', 'cup', 'book', 'bag']
['bag', 'book', 'cup', 'pen']
```

`ORDER BY ?` hata vermedi ama sıralamadı da: değer sabit bir metin olarak
alındı, bütün satırlar için aynı olduğu için sıra eklendiği gibi kaldı.
Çözüm bir **izin listesidir**: kullanıcının seçimi yalnızca bilinen
sütunlardan birine **eşlenir**, sorguya giren metin her zaman bizim
yazdığımız metindir. Listede olmayan bir seçim (`rating`) varsayılana
düştü.

## Parametrenin yetmediği yer 2: LIKE joker karakterleri

`LIKE` aramasında `%` "herhangi bir metin", `_` "herhangi bir karakter"
demektir. Parametreli sorgu kullanıcının girdisini kod yapmaz ama bu
işaretler **LIKE'ın kendi dilinde** yine joker olarak çalışır:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE notes (text TEXT)")
conn.executemany("INSERT INTO notes VALUES (?)",
                 [("50% discount",), ("500 pens",), ("plan_b",), ("planner",)])


def search(term):
    rows = conn.execute("SELECT text FROM notes WHERE text LIKE ?",
                        ("%" + term + "%",))
    return [r[0] for r in rows]


def escape_like(term):
    return term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search_exact(term):
    rows = conn.execute("SELECT text FROM notes WHERE text LIKE ? ESCAPE '\\'",
                        ("%" + escape_like(term) + "%",))
    return [r[0] for r in rows]


print(search("%"))
print(search("0%"))
print(search_exact("0%"))
print(search("_"))
print(search_exact("_"))
```

```text
['50% discount', '500 pens', 'plan_b', 'planner']
['50% discount', '500 pens']
['50% discount']
['50% discount', '500 pens', 'plan_b', 'planner']
['plan_b']
```

`%` araması bütün notları getirdi; `0%` "içinde 0 geçen her şey" oldu.
Joker işaretleri bir **kaçış karakteriyle** (`\`) önüne işaret konarak
etkisizleştirildi ve sorguya `ESCAPE '\'` eklendi; artık `%` ve `_` düz
karakter olarak aranıyor. Kaçış karakterinin kendisi **önce** kaçılır,
yoksa kullanıcının yazdığı `\` bir sonraki karakteri etkisizleştirir. Bu
açık veri sızdırmaz ama aramayı yanlış çalıştırır ve çok geniş bir
`LIKE` deseni büyük tablolarda veritabanını yorabilir.

## Parametrenin yetmediği yer 3: ikinci dereceden enjeksiyon

Bir değer ilk kez kaydedilirken parametreyle güvenle yazılır; ama daha
sonra **veritabanından okunup** başka bir sorguya metinle eklenirse açık
o ikinci sorguda ortaya çıkar. "Bu değer zaten bizim veritabanımızdan
geliyor" düşüncesi yanıltır: değerin kaynağı yine kullanıcıdır. Kural
basit: **her** sorguda, değer nereden gelirse gelsin, parametre.

## Zararı sınırlamak

Açık bir yerde gözden kaçsa bile zararı küçültmek için katmanlar vardır:

- **En az yetki:** uygulamanın veritabanı kullanıcısı yalnızca gereken
  tablolarda, yalnızca gereken işlemleri yapabilir. Rapor üreten bir
  bölüm yalnızca okur:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (item TEXT)")
conn.execute("INSERT INTO orders VALUES ('book')")
conn.execute("PRAGMA query_only = ON")

print(conn.execute("SELECT item FROM orders").fetchall())
try:
    conn.execute("DELETE FROM orders")
except sqlite3.OperationalError as error:
    print("refused:", error)
```

```text
[('book',)]
refused: attempt to write a readonly database
```

- **Hata ayrıntısını gizlemek:** veritabanı hata mesajı (tablo adları,
  sorgunun parçası) kullanıcıya gösterilmez; kullanıcı genel bir mesaj
  görür, ayrıntı sunucunun kaydına yazılır. Ayrıntılı hata mesajı
  saldırganın sorguyu adım adım çözmesine yardım eder.
- **Girdi doğrulama:** sipariş numarası bir tam sayıysa önce tam sayıya
  çevrilir; e-posta alanı e-posta biçiminde mi bakılır (Girdi Doğrulama
  bölümü). Bu parametrenin **yerine** değil, **yanında** bir katmandır.
- **WAF ve izleme:** bilinen kalıpları yakalayabilir ama atlatılabilir
  (Güvenlik Duvarı bölümü); asıl düzeltme koddadır.

## Özet

- SQL enjeksiyonu: sorgu metinle kurulunca girdideki işaretler **sorgunun
  anlamını** değiştirir; derste 4 siparişin hepsi geldi.
- **Parametreli sorgu** (`?` ve ayrı değerler) kalıcı çözümdür; değer ne
  olursa olsun veri kalır.
- Yer tutucu **sütun ve tablo adının** yerine geçmez: kullanıcının seçimi
  bir **izin listesine** eşlenir.
- **LIKE** içinde `%` ve `_` joker kalır: önce kaçış karakteri, sonra `%`
  ve `_` kaçılır, `ESCAPE` yazılır.
- **İkinci dereceden** enjeksiyona karşı veritabanından gelen değer de
  parametreyle kullanılır.
- Zararı sınırlayan katmanlar: en az yetkili veritabanı kullanıcısı, genel
  hata mesajı, girdi doğrulama, izleme.
