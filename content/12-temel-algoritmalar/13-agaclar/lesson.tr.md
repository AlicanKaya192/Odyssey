# Ağaçlar

Bilgisayarındaki klasörler, bir web sayfasının HTML'i, bir şirketin
organizasyon şeması: hepsi **hiyerarşi**. Bir üst, altında birkaç alt, onların
da altları. Bu yapının adı **ağaç (tree)**.

Bağlı listede her düğümün tek bir "sonraki"si vardı. Ağaçta bir düğümün
**birden çok çocuğu** olabilir. Veri biliminde de sık karşına çıkacak: karar
ağacı (decision tree), rastgele orman (random forest) ve gradyan artırma
(gradient boosting) modellerinin hepsi ağaç.

## Terimler

<figure class="fig">
<svg viewBox="0 0 350 180" width="350" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="135.0" y2="153.0"/>
<line class="line" x1="247.0" y1="89.0" x2="303.0" y2="153.0"/>
<line class="line" x1="191.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="191.0" y1="25.0" x2="247.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<circle class="curve4" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">2</text>
<circle class="box" cx="135.0" cy="153.0" r="17"/>
<circle class="curve4" cx="135.0" cy="153.0" r="17"/>
<text class="ink" x="135.0" y="157.9" font-size="14" text-anchor="middle">5</text>
<circle class="box" cx="191.0" cy="25.0" r="17"/>
<circle class="curve" cx="191.0" cy="25.0" r="17"/>
<text class="ink" x="191.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="247.0" cy="89.0" r="17"/>
<text class="ink" x="247.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="303.0" cy="153.0" r="17"/>
<circle class="curve4" cx="303.0" cy="153.0" r="17"/>
<text class="ink" x="303.0" y="157.9" font-size="14" text-anchor="middle">6</text>
</svg>
<figcaption>Mor halka kök, yeşil halkalar yapraklar. 2, 4 ve 5 birlikte bir alt ağaç.</figcaption>
</figure>

- **Kök (root):** en üstteki düğüm, ebeveyni yok. Burada `1`.
- **Ebeveyn (parent) ve çocuk (child):** `2`, `4` ile `5`'in ebeveyni; `4` ve
  `5`, `2`'nin çocukları.
- **Yaprak (leaf):** çocuğu olmayan düğüm. Burada `4`, `5`, `6`.
- **Alt ağaç (subtree):** bir düğüm ve altındaki her şey. `2`, `4`, `5` bir
  alt ağaç; kendisi de bir ağaç.
- **Derinlik (depth):** bir düğümün köke uzaklığı (kök 0). **Yükseklik
  (height):** ağaçtaki en uzun kökten yaprağa yolun düğüm sayısı; bu ağaçta 3.

Her düğümün **en fazla iki** çocuğu varsa ağaca **ikili ağaç (binary tree)**
denir; çocuklara **sol** ve **sağ** denir. Bu bölümde ikili ağaçla
çalışacağız.

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

root = TreeNode(1,
                TreeNode(2, TreeNode(4), TreeNode(5)),
                TreeNode(3, None, TreeNode(6)))
```

Bağlı listedeki `Node`'un aynısı, yalnızca `next` yerine `left` ve `right`
var. Boş çocuk `None`.

## Özyineleme ağacın doğal dili

Ağacın tanımı kendini içeriyor: bir ağaç ya **boştur** ya da bir kök ve **iki
alt ağaçtır**. Özyineleme bölümündeki kalıp buraya birebir oturur:

- **Taban durumu:** boş ağaç (`None`).
- **Özyineli adım:** iki çocuktan cevabı al, kendi düğümünle birleştir.

```python
def size(node):                    # düğüm sayısı
    if node is None:
        return 0
    return 1 + size(node.left) + size(node.right)

def height(node):                  # yükseklik
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))

print(size(root), height(root))
```

```text
6 3
```

İkisi de her düğüme bir kez uğrar: `O(n)`. Ağaçla ilgili sorunların çoğu bu
iki satırlık iskeletle çözülür; değişen yalnızca "birleştir" kısmı (toplam,
en büyük, sayaç…).

## Derinlemesine gezinme: üç sıra

Bütün düğümleri gezmenin üç klasik sırası var. Fark, düğümün kendisinin
çocuklarından **önce mi, arada mı, sonra mı** yazıldığı:

```python
def preorder(node):                # önce kök, sonra sol, sonra sağ
    if node is None:
        return []
    return [node.value] + preorder(node.left) + preorder(node.right)

def inorder(node):                 # sol, kök, sağ
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)

def postorder(node):               # sol, sağ, en son kök
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.value]

print("preorder :", preorder(root))
print("inorder  :", inorder(root))
print("postorder:", postorder(root))
```

```text
preorder : [1, 2, 4, 5, 3, 6]
inorder  : [4, 2, 5, 1, 3, 6]
postorder: [4, 5, 2, 6, 3, 1]
```

Her biri ayrı bir işe yarar:

- **Preorder (önce kök):** yapıyı yukarıdan aşağı kopyalamak ya da yazdırmak
  (klasör ağacını girintili listelemek gibi).
- **Inorder (ortada kök):** bir sonraki bölümdeki **ikili arama ağacında**
  değerleri **sıralı** verir.
- **Postorder (en son kök):** önce çocukların cevabı gerekiyorsa; bir
  klasörün boyutu, içindekilerin boyutu bilinmeden hesaplanamaz.

Üçü de bir yola girip **dibine kadar** iner, sonra geri döner. Bu yüzden
hepsine **derinlemesine arama (depth-first search, DFS)** denir.

## Genişlemesine gezinme: seviye seviye

Bazen ağacı kat kat okumak istersin: önce kök, sonra onun çocukları, sonra
torunlar. Buna **genişlemesine arama (breadth-first search, BFS)** denir ve
aracı Yığın ve Kuyruk bölümündeki **kuyruk**: ilk giren ilk işlenir.

<figure class="fig">
<svg viewBox="0 0 424 180" width="424" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="30" font-size="12">seviye 0</text>
<text class="dim" x="4" y="94" font-size="12">seviye 1</text>
<text class="dim" x="4" y="158" font-size="12">seviye 2</text>
<line class="line" x1="153.0" y1="89.0" x2="97.0" y2="153.0"/>
<line class="line" x1="153.0" y1="89.0" x2="209.0" y2="153.0"/>
<line class="line" x1="321.0" y1="89.0" x2="377.0" y2="153.0"/>
<line class="line" x1="265.0" y1="25.0" x2="153.0" y2="89.0"/>
<line class="line" x1="265.0" y1="25.0" x2="321.0" y2="89.0"/>
<circle class="box" cx="97.0" cy="153.0" r="17"/>
<text class="ink" x="97.0" y="157.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="153.0" cy="89.0" r="17"/>
<text class="ink" x="153.0" y="93.9" font-size="14" text-anchor="middle">2</text>
<circle class="box" cx="209.0" cy="153.0" r="17"/>
<text class="ink" x="209.0" y="157.9" font-size="14" text-anchor="middle">5</text>
<circle class="box" cx="265.0" cy="25.0" r="17"/>
<text class="ink" x="265.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="321.0" cy="89.0" r="17"/>
<text class="ink" x="321.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="377.0" cy="153.0" r="17"/>
<text class="ink" x="377.0" y="157.9" font-size="14" text-anchor="middle">6</text>
</svg>
<figcaption>BFS önce seviye 0'ı, sonra seviye 1'i, sonra seviye 2'yi soldan sağa okur.</figcaption>
</figure>

```python
from collections import deque

def level_order(root):
    if root is None:
        return []
    levels = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):        # şu an kuyrukta olanlar = bu seviye
            node = queue.popleft()
            level.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels

print(level_order(root))
```

```text
[[1], [2, 3], [4, 5, 6]]
```

Püf noktası `for _ in range(len(queue))`: iç döngü başlarken kuyrukta
**yalnızca bu seviyenin** düğümleri var; onların çocukları kuyruğun arkasına
eklenir ve bir sonraki turda işlenir.

## Özyinelemesiz DFS: yığınla

Özyinelemede çağrı yığınını Python tutuyordu. Aynı işi açık bir **yığınla**
kendin de yapabilirsin:

```python
def preorder_iter(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.value)
        if node.right:                 # önce sağ: yığından en son çıkar
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out

print(preorder_iter(root))
```

```text
[1, 2, 4, 5, 3, 6]
```

Sonuç özyineli `preorder` ile aynı. Kuyruk BFS'i, yığın DFS'i verir: iki
gezinme arasındaki tek fark hangi uçtan alındığı. Graflar bölümünde bu ikisi
yine karşımıza çıkacak.

## Yükseklik neden önemli?

Ağaçta işlerin çoğu kökten bir yaprağa doğru yürür; maliyet **yükseklik
(`h`)** kadardır. Aynı sayıda düğüm iki çok farklı yükseklikte dizilebilir:

```text
balanced: 511 nodes, height 9
chain   : 511 nodes, height 511
chain of 5000 nodes: RecursionError
```

511 düğüm **dengeli (balanced)** dizilince yükseklik 9: her seviye bir
öncekinin iki katı düğüm alır, `h ≈ log₂ n`. Her düğümün tek çocuğu varsa ağaç
aslında bir bağlı listedir, `h = n`. Bir de pratik bedeli var: 5000 düğümlük
zincirde özyineli `height` Python'un özyineleme sınırına takıldı
(`RecursionError`). Bir sonraki bölümde, ağacın dengeli kalması neden bu kadar
önemsenir, onu göreceğiz.

## Veri biliminde ağaç: karar ağacı

Bir **karar ağacı** her iç düğümde bir soru sorar ("taç yaprağı uzunluğu
en fazla 2,5 mi?"), cevaba göre sola ya da sağa gider; yaprakta tahmin
yazar. Aşağıdaki küçük ağaç iris çiçeklerini üç türe ayırıyor:

<figure class="fig">
<svg viewBox="0 0 575 180" width="575" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="370.6" y1="89.0" x2="275.6" y2="153.0"/>
<text class="dim" x="313.1" y="121.0" font-size="12" text-anchor="end">evet</text>
<line class="line" x1="370.6" y1="89.0" x2="465.6" y2="153.0"/>
<text class="dim" x="428.1" y="121.0" font-size="12" text-anchor="start">hayır</text>
<line class="line" x1="180.6" y1="25.0" x2="85.6" y2="89.0"/>
<text class="dim" x="123.1" y="57.0" font-size="12" text-anchor="end">evet</text>
<line class="line" x1="180.6" y1="25.0" x2="370.6" y2="89.0"/>
<text class="dim" x="285.6" y="57.0" font-size="12" text-anchor="start">hayır</text>
<rect class="box" x="53.0" y="72.0" width="65.0" height="34" rx="8"/>
<rect class="curve4" x="53.0" y="72.0" width="65.0" height="34" rx="8"/>
<text class="ink" x="85.6" y="93.9" font-size="14" text-anchor="middle">setosa</text>
<rect class="box" x="101.0" y="8.0" width="159.1" height="34" rx="8"/>
<text class="ink" x="180.6" y="29.9" font-size="14" text-anchor="middle">petal_length ≤ 2.5</text>
<rect class="box" x="227.4" y="136.0" width="96.4" height="34" rx="8"/>
<rect class="curve4" x="227.4" y="136.0" width="96.4" height="34" rx="8"/>
<text class="ink" x="275.6" y="157.9" font-size="14" text-anchor="middle">versicolor</text>
<rect class="box" x="291.0" y="72.0" width="159.1" height="34" rx="8"/>
<text class="ink" x="370.6" y="93.9" font-size="14" text-anchor="middle">petal_width ≤ 1.75</text>
<rect class="box" x="421.3" y="136.0" width="88.6" height="34" rx="8"/>
<rect class="curve4" x="421.3" y="136.0" width="88.6" height="34" rx="8"/>
<text class="ink" x="465.6" y="157.9" font-size="14" text-anchor="middle">virginica</text>
</svg>
<figcaption>İç düğümler soru sorar, yeşil halkalı yapraklar tahmini verir. Cevap evetse sola, hayırsa sağa.</figcaption>
</figure>

Ağacı iç içe sözlükle tutabiliriz; tahmin etmek, kökten bir yaprağa yürümek:

```python
tree = {
    "feature": "petal_length", "threshold": 2.5,
    "left": "setosa",
    "right": {
        "feature": "petal_width", "threshold": 1.75,
        "left": "versicolor",
        "right": "virginica",
    },
}

def predict(node, flower):
    while isinstance(node, dict):          # yaprak bir metin
        if flower[node["feature"]] <= node["threshold"]:
            node = node["left"]
        else:
            node = node["right"]
    return node

print(predict(tree, {"petal_length": 1.4, "petal_width": 0.2}))
print(predict(tree, {"petal_length": 4.5, "petal_width": 1.5}))
print(predict(tree, {"petal_length": 5.8, "petal_width": 2.2}))
```

```text
setosa
versicolor
virginica
```

scikit-learn'ün `DecisionTreeClassifier`'ı da tahmin ederken tam olarak bunu
yapar; maliyet ağacın **derinliği** kadar, veri setinin boyutundan bağımsız.
Ağacın soruları veriden nasıl seçtiğini ML Algoritmaları modülünde sıfırdan kuracağız.

## Özet

- Ağaç: hiyerarşi; kök, çocuk, yaprak, alt ağaç. İkili ağaçta en fazla iki
  çocuk.
- Özyineli iskelet: `None` ise taban durumu, değilse iki çocuğun cevabını
  birleştir. `O(n)`.
- DFS: preorder (kök önce), inorder (ortada), postorder (sonda); yığınla
  özyinelemesiz de yazılır.
- BFS: kuyrukla seviye seviye; `for _ in range(len(queue))` bir seviyeyi
  ayırır.
- Kökten yaprağa işler `O(h)`: dengeli ağaçta `h ≈ log₂ n`, zincirde `h = n`.
- Karar ağacında tahmin, kökten yaprağa bir yürüyüş.
