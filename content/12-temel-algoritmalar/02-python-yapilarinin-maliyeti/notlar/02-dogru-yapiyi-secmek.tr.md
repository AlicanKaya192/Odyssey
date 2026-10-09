Bir problemde hangi yapıyı kullanacağına çoğu zaman **en sık soracağın
soru** karar verir.

| En sık soru / iş | Yapı | Neden |
|---|---|---|
| "i'inci eleman ne?" | `list` | indeksle `O(1)` |
| "Sona ekle, sırayla gez" | `list` | `append` amortize `O(1)` |
| "Bu değer daha önce görüldü mü?" | `set` | `in` ortalama `O(1)` |
| "Bu anahtarın değeri ne?" (sayaç, eşleme) | `dict` | ortalama `O(1)` |
| "İlk gelen ilk çıksın" (kuyruk) | `collections.deque` | `popleft` `O(1)` |
| "Son giren ilk çıksın" (yığın) | `list` (`append` + `pop`) | sondan `O(1)` |
| "Hep en küçüğü/en büyüğü ver" | `heapq` | Öncelik Kuyruğu bölümünde |
| "Sıralı tut, içinde ara" | sıralı `list` + `bisect` | Arama bölümünde |

## Örnek: hangi yapı?

**1. Bir sitede bugün giriş yapan kullanıcıların adları geliyor; her yeni
girişte "bu kişi bugün ilk kez mi geldi?" diye soracağız.**
→ `set`. Liste olsa her girişte bütün listeyi tarardık.

**2. Bir kelime listesinde her kelimenin kaç kez geçtiğini sayacağız.**
→ `dict` (ya da `collections.Counter`). Her kelime için `items.count(w)`
çağırmak `O(n²)` olurdu.

**3. Bir yazıcıya sırayla gelen işler var; ilk gelen ilk basılacak.**
→ `deque`. Listeden `pop(0)` her seferinde bütün listeyi kaydırır.

**4. Bir listede sık sık "75. sıradaki kayıt" soruluyor.**
→ `list`. Küme sıra tutmaz, `deque`'de ortaya erişmek yavaş.

## İki yapıyı birlikte kullanmak

Bazen tek yapı yetmez: "tekrarları ayıkla ama **sırayı koru**" isteğinde
sıra için bir **liste**, "görüldü mü?" sorusu için bir **küme** tutulur.
Derste `unique_with_set` tam olarak buydu. Ek bellek `O(n)`; karşılığında
`O(n²)` iş `O(n)`'e iner.

Not: Python 3.7'den beri `dict` ekleme sırasını korur; bu yüzden
`list(dict.fromkeys(items))` da tekrarları sırayı koruyarak ayıklar.
