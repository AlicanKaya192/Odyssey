Dört aracın seçenekleri, bir bakışta.

## sort

| Yazım | Ne yapar |
|---|---|
| `sort f` | Abece sırası (metin gibi) |
| `sort -r f` | Ters sıra |
| `sort -n f` | Sayı değerine göre |
| `sort -u f` | Sıralar ve tekrarları atar |
| `sort -t , -k 3 f` | Virgülle ayrılmış 3. alandan itibaren |
| `sort -t , -k 3,3 f` | Yalnızca 3. alana göre |
| `sort -t , -k 3 -rn f` | 3. alana göre, büyükten küçüğe |

## uniq

| Yazım | Ne yapar |
|---|---|
| `uniq` | Art arda aynı satırları teke indirir |
| `uniq -c` | Önüne tekrar sayısını yazar |
| `uniq -d` | Yalnızca tekrarlananlar (birer kez) |
| `uniq -u` | Yalnızca bir kez geçenler |
| `uniq -i` | Harf büyüklüğüne bakmadan |

Hemen her zaman önünde `sort` durur.

## cut

| Yazım | Ne yapar |
|---|---|
| `cut -d , -f 2` | 2. alan |
| `cut -d , -f 1,3` | 1. ve 3. alanlar |
| `cut -d , -f 2-4` | 2'den 4'e |
| `cut -d ' ' -f 3-` | 3. alandan sona |
| `cut -c 1-10` | İlk 10 karakter |

Ayırıcı verilmezse sekme (`Tab`) sayılır.

## tr

| Yazım | Ne yapar |
|---|---|
| `tr a-z A-Z` | Küçük harfi büyüğe |
| `tr '[:upper:]' '[:lower:]'` | Büyük harfi küçüğe |
| `tr -d '0-9'` | Rakamları siler |
| `tr -s ' '` | Art arda boşlukları teke indirir |
| `tr , '\n'` | Virgülü satır sonuna çevirir |

`tr` dosya adı almaz: `tr ... < f` ya da <code>cat f &#124; tr ...</code>.
