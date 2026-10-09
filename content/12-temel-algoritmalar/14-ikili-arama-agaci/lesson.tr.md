# İkili Arama Ağacı

Sıralı listede ikili arama `O(log n)` sürüyordu, ama araya eleman eklemek
kaydırma yüzünden `O(n)`. Sözlük ekleme ve aramayı `O(1)`'de yapıyor, ama
**sırayı** bilmiyor: "6'dan büyük en küçük değer" ya da "4 ile 10 arasındakiler"
sorularına cevap veremiyor. **İkili arama ağacı (binary search tree, BST)**
ikisinin arasında duruyor: ağaç dengeli kaldıkça arama, ekleme ve silme
`O(log n)`, üstelik sıra korunuyor.

## Tek kural

Her düğüm için: **sol alt ağaçtaki bütün değerler düğümden küçük, sağ alt
ağaçtaki bütün değerler düğümden büyük.** Kural yalnızca çocuklar için değil,
**alt ağacın tamamı** için geçerli.

<figure class="fig">
<svg viewBox="0 0 518 244" width="518" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="191.0" y1="153.0" x2="135.0" y2="217.0"/>
<line class="line" x1="191.0" y1="153.0" x2="247.0" y2="217.0"/>
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="191.0" y2="153.0"/>
<line class="line" x1="471.0" y1="153.0" x2="415.0" y2="217.0"/>
<line class="line" x1="359.0" y1="89.0" x2="471.0" y2="153.0"/>
<line class="line" x1="303.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="303.0" y1="25.0" x2="359.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<circle class="curve" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="135.0" cy="217.0" r="17"/>
<text class="ink" x="135.0" y="221.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="191.0" cy="153.0" r="17"/>
<circle class="curve" cx="191.0" cy="153.0" r="17"/>
<text class="ink" x="191.0" y="157.9" font-size="14" text-anchor="middle">6</text>
<circle class="box" cx="247.0" cy="217.0" r="17"/>
<text class="ink" x="247.0" y="221.9" font-size="14" text-anchor="middle">7</text>
<circle class="box" cx="303.0" cy="25.0" r="17"/>
<circle class="curve" cx="303.0" cy="25.0" r="17"/>
<text class="ink" x="303.0" y="29.9" font-size="14" text-anchor="middle">8</text>
<circle class="box" cx="359.0" cy="89.0" r="17"/>
<text class="ink" x="359.0" y="93.9" font-size="14" text-anchor="middle">10</text>
<circle class="box" cx="415.0" cy="217.0" r="17"/>
<text class="ink" x="415.0" y="221.9" font-size="14" text-anchor="middle">13</text>
<circle class="box" cx="471.0" cy="153.0" r="17"/>
<text class="ink" x="471.0" y="157.9" font-size="14" text-anchor="middle">14</text>
</svg>
<figcaption>8, 3, 10, 1, 6, 14, 4, 7, 13 sırayla eklenince oluşan ağaç. Mor halkalar 6'yı arama yolu: 6 &lt; 8 sola, 6 &gt; 3 sağa.</figcaption>
</figure>

Bu kuralın hediyesi, Ağaçlar bölümündeki **inorder** gezinmede: sol, kök, sağ
sırası değerleri **küçükten büyüğe** verir.

## Ekleme

Yeni değer, kökten başlayıp kurala göre sola ya da sağa inerek boş bir yere
konur. Ağaç bölümündeki özyineli iskeletin aynısı:

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def insert(node, value):
    if node is None:                       # boş yer bulundu
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node                            # eşitse ekleme: tekrar yok

def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)

root = None
for v in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    root = insert(root, v)
print(inorder(root))
```

```text
[1, 3, 4, 6, 7, 8, 10, 13, 14]
```

Değerler karışık sırayla geldi, inorder sıralı verdi. Bu ağaç, yukarıdaki
şekildeki ağaç.

## Arama

Her adımda bir alt ağacın tamamı elenir, tıpkı ikili aramada listenin yarısı
gibi:

```python
def search(node, target):
    path = []
    while node:
        path.append(node.value)
        if target == node.value:
            return True, path
        node = node.left if target < node.value else node.right
    return False, path

print(search(root, 6))
print(search(root, 5))
```

```text
(True, [8, 3, 6])
(False, [8, 3, 6, 4])
```

`6` üç adımda bulundu (şekilde mor halkalı yol). `5` yoksa bile çok
aranmadı: `4`'ün sağı boş, `5` varsa orada olurdu. Adım sayısı en fazla
ağacın **yüksekliği** kadar: `O(h)`.

En küçük değer en soldaki düğümde, en büyük en sağdakinde:

```python
def minimum(node):
    while node.left:
        node = node.left
    return node.value
```

## Silme: üç durum

Silmek en zor işlem, çünkü düğüm çıkınca kural bozulmamalı:

1. **Yaprak:** doğrudan çıkarılır.
2. **Tek çocuk:** çocuk, silinen düğümün yerine geçer.
3. **İki çocuk:** düğümün yerine **sıradaki değer (inorder successor)**
   konur: sağ alt ağacın en küçüğü. O değer düğümden büyük ama sağ alt
   ağaçtaki her şeyden küçük, yani kural korunur. Sonra o değer sağ alt
   ağaçtan silinir (orada en fazla bir çocuğu vardır).

<figure class="fig">
<svg viewBox="0 0 518 244" width="518" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="191.0" y1="153.0" x2="135.0" y2="217.0"/>
<line class="line" x1="191.0" y1="153.0" x2="247.0" y2="217.0"/>
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="191.0" y2="153.0"/>
<line class="line" x1="471.0" y1="153.0" x2="415.0" y2="217.0"/>
<line class="line" x1="359.0" y1="89.0" x2="471.0" y2="153.0"/>
<line class="line" x1="303.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="303.0" y1="25.0" x2="359.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<circle class="curve2" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="135.0" cy="217.0" r="17"/>
<circle class="curve4" cx="135.0" cy="217.0" r="17"/>
<text class="ink" x="135.0" y="221.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="191.0" cy="153.0" r="17"/>
<text class="ink" x="191.0" y="157.9" font-size="14" text-anchor="middle">6</text>
<circle class="box" cx="247.0" cy="217.0" r="17"/>
<text class="ink" x="247.0" y="221.9" font-size="14" text-anchor="middle">7</text>
<circle class="box" cx="303.0" cy="25.0" r="17"/>
<text class="ink" x="303.0" y="29.9" font-size="14" text-anchor="middle">8</text>
<circle class="box" cx="359.0" cy="89.0" r="17"/>
<text class="ink" x="359.0" y="93.9" font-size="14" text-anchor="middle">10</text>
<circle class="box" cx="415.0" cy="217.0" r="17"/>
<text class="ink" x="415.0" y="221.9" font-size="14" text-anchor="middle">13</text>
<circle class="box" cx="471.0" cy="153.0" r="17"/>
<text class="ink" x="471.0" y="157.9" font-size="14" text-anchor="middle">14</text>
</svg>
<figcaption>Turuncu halkalı 3'ün iki çocuğu var. Yerine sağ alt ağacının en küçüğü, yeşil halkalı 4 geçer.</figcaption>
</figure>

```python
def delete(node, value):
    if node is None:
        return None
    if value < node.value:
        node.left = delete(node.left, value)
    elif value > node.value:
        node.right = delete(node.right, value)
    else:
        if node.left is None:              # 1 ve 2: en fazla bir çocuk
            return node.right
        if node.right is None:
            return node.left
        successor = minimum(node.right)    # 3: iki çocuk
        node.value = successor
        node.right = delete(node.right, successor)
    return node

for v in [7, 14, 3]:
    root = delete(root, v)
    print("delete", v, "->", inorder(root))
print("root:", root.value, "left:", root.left.value)
```

```text
delete 7 -> [1, 3, 4, 6, 8, 10, 13, 14]
delete 14 -> [1, 3, 4, 6, 8, 10, 13]
delete 3 -> [1, 4, 6, 8, 10, 13]
root: 8 left: 4
```

`7` yapraktı, `14`'ün tek çocuğu (`13`) vardı, `3`'ün iki çocuğu vardı: yerine
sağ alt ağacının en küçüğü `4` geçti. Üç silmeden sonra inorder hâlâ sıralı.

## Ekleme sırası her şeyi değiştirir

Aynı değerler farklı sırayla eklenince ağacın şekli değişir. Değerler
**sıralı** gelirse her yeni değer bir öncekinin sağına konur ve ağaç bir
zincire döner:

<figure class="fig">
<svg viewBox="0 0 254 236" width="254" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="161.0" y1="163.0" x2="207.0" y2="209.0"/>
<line class="line" x1="115.0" y1="117.0" x2="161.0" y2="163.0"/>
<line class="line" x1="69.0" y1="71.0" x2="115.0" y2="117.0"/>
<line class="line" x1="23.0" y1="25.0" x2="69.0" y2="71.0"/>
<circle class="box" cx="23.0" cy="25.0" r="17"/>
<text class="ink" x="23.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="69.0" cy="71.0" r="17"/>
<text class="ink" x="69.0" y="75.9" font-size="14" text-anchor="middle">2</text>
<circle class="box" cx="115.0" cy="117.0" r="17"/>
<text class="ink" x="115.0" y="121.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="161.0" cy="163.0" r="17"/>
<text class="ink" x="161.0" y="167.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="207.0" cy="209.0" r="17"/>
<text class="ink" x="207.0" y="213.9" font-size="14" text-anchor="middle">5</text>
</svg>
<figcaption>1, 2, 3, 4, 5 sırayla eklenince her değer bir öncekinin sağına düşer: yükseklik 5.</figcaption>
</figure>

0'dan 1999'a kadar 2000 sayıyı iki sırayla ekleyip ölçtük:

```text
mixed  order: height 24 | steps to find 1999: 9
sorted order: height 2000 | steps to find 1999: 2000
```

Karışık sırada yükseklik 24, `1999`'u bulmak 9 adım. Sıralı sırada yükseklik
2000: ağaç artık bir bağlı liste ve arama `O(n)`. Gerçek veride bu sık olur:
tarihe göre gelen kayıtlar, artan sipariş numaraları zaten sıralıdır.

## Dengeli ağaçlar

Çözüm, ağacı her eklemede ve silmede **dengede tutmak**. **AVL ağacı** ve
**kırmızı-siyah ağaç (red-black tree)** bunu **döndürme (rotation)** denen
küçük yeniden bağlamalarla yapar: bir taraf fazla uzayınca birkaç bağlantıyı
çevirip yüksekliği `O(log n)`'de tutar. Kodları uzun ve ayrıntılıdır; burada
fikri bilmek yeterli:

- Dengeli bir BST'de arama, ekleme, silme **her zaman** `O(log n)`.
- Java'nın `TreeMap`'i, C++'ın `std::map`'i genellikle kırmızı-siyah ağaçtır.
- Veritabanı indeksleri (SQL patikasındaki `CREATE INDEX`) bunun disk için
  geliştirilmiş hâli **B-ağacı (B-tree)** ile çalışır: bir düğümde yüzlerce
  anahtar, böylece milyonlarca satırda bile ağaç yalnızca birkaç seviye.

Python'un standart kütüphanesinde dengeli ağaç yok. Sıralı bir koleksiyon
gerekince çoğu zaman **sıralı liste + `bisect`** yeter: arama `O(log n)`,
ekleme kaydırma yüzünden `O(n)` ama C hızında. Çok büyük ve sık değişen
koleksiyonlar için üçüncü taraf `sortedcontainers` paketi var.

## Veri biliminde: en yakın komşu

k-en yakın komşu (k-nearest neighbors, KNN) bir noktaya en yakın örnekleri
arar. Bütün veri setini taramak her tahminde `O(n)`. scikit-learn bunun için
BST fikrinin çok boyutlu hâlini kullanır: **k-d ağacı (k-d tree)** her
seviyede bir başka özelliğe göre sola/sağa ayırır ve uzak bölgeleri hiç
gezmeden eler. `KNeighborsClassifier(algorithm="kd_tree")` bu ağacı kurar.

## Özet

- BST kuralı: sol alt ağaç küçük, sağ alt ağaç büyük; **bütün** alt ağaç için.
- Inorder gezinme değerleri sıralı verir.
- Arama, ekleme, silme `O(h)`. Silmede iki çocuklu düğüme sıradaki değer
  (sağ alt ağacın en küçüğü) geçer.
- Sıralı eklenen değerler zincir yapar, `h = n`. Dengeli ağaçlar (AVL,
  kırmızı-siyah) döndürmelerle `h = O(log n)` tutar; veritabanları B-ağacı
  kullanır.
- Python'da çoğu iş için sıralı liste + `bisect` yeter.
