# Metin Algoritmaları

Bir metinde bir kelimeyi aramak, binlerce belgede kopya paragraf bulmak,
arama kutusunda yazdığın harflere göre öneri çıkarmak: hepsi metin üzerinde
çalışan algoritmalar. Python'un `in` ve `str.find`'ı işini görür, ama
arkalarındaki fikirleri bilmek, hazır bir fonksiyonun yetmediği yerde (çok
sayıda kalıp, önek araması, benzer belge) doğru aracı seçmeni sağlar.

Bu bölümde **metin (text)** uzunluğu `n`, aranan **kalıp (pattern)** uzunluğu
`m`.

## Saf arama: her konumdan dene

En basit yol: kalıbı metnin her konumuna koy ve harf harf karşılaştır.

```python
def naive_search(text, pattern):
    found, checks = [], 0
    for i in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern):
            checks += 1                     # bir harf karşılaştırması
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == len(pattern):
            found.append(i)
    return found, checks


print(naive_search("abracadabra", "abra"))
```

```text
([0, 7], 16)
```

İki eşleşme (0 ve 7. konumlar) ve 16 karşılaştırma. Konumların çoğu ilk harfte
eleniyorsa saf arama hızlıdır. Ama kötü durumda her konumda kalıbın neredeyse
tamamı karşılaştırılır: `O(n · m)`.

## KMP: geri dönmeden ilerle

Saf arama bir uyuşmazlıkta metinde geri gider ve az önce okuduğu harfleri
yeniden okur. **KMP (Knuth–Morris–Pratt)** bunu yapmaz: kalıbın kendi içindeki
tekrarı önceden bir tabloya yazar. Tablonun `i`. hücresi, kalıbın ilk `i + 1`
harfinin hem **öneki** hem **soneki** olan en uzun parçanın boyudur.

<figure class="fig">
<div><svg viewBox="0 0 350 66" width="350" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">pattern</text>
<text class="dim" x="93.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="46" height="36"/>
<text class="ink" x="93.0" y="48.9" font-size="14" text-anchor="middle">a</text>
<text class="dim" x="139.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="116" y="26" width="46" height="36"/>
<text class="ink" x="139.0" y="48.9" font-size="14" text-anchor="middle">b</text>
<text class="dim" x="185.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="162" y="26" width="46" height="36"/>
<text class="ink" x="185.0" y="48.9" font-size="14" text-anchor="middle">a</text>
<text class="dim" x="231.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="208" y="26" width="46" height="36"/>
<text class="ink" x="231.0" y="48.9" font-size="14" text-anchor="middle">c</text>
<text class="dim" x="277.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="254" y="26" width="46" height="36"/>
<text class="ink" x="277.0" y="48.9" font-size="14" text-anchor="middle">a</text>
<text class="dim" x="323.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="300" y="26" width="46" height="36"/>
<text class="ink" x="323.0" y="48.9" font-size="14" text-anchor="middle">b</text>
</svg></div><div><svg viewBox="0 0 350 66" width="350" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">table</text>
<text class="dim" x="93.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="46" height="36"/>
<text class="ink" x="93.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="139.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="116" y="26" width="46" height="36"/>
<text class="ink" x="139.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="185.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="162" y="26" width="46" height="36"/>
<text class="ink" x="185.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="231.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="208" y="26" width="46" height="36"/>
<text class="ink" x="231.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="277.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="254" y="26" width="46" height="36"/>
<rect class="curve" x="256" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="277.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="323.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="300" y="26" width="46" height="36"/>
<rect class="curve" x="302" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="323.0" y="48.9" font-size="14" text-anchor="middle">2</text>
</svg></div>
<figcaption><code>abacab</code> için tablo. Son hücre 2: <code>ab</code> hem baştaki hem sondaki parça. Uyuşmazlıkta kalıp, baştan değil 2. harften devam eder.</figcaption>
</figure>

Uyuşmazlıkta bu tablo "kalıbın ne kadarı zaten eşleşmiş sayılabilir"
sorusunu cevaplar; metinde hiç geri gidilmez.

```python
def prefix_table(pattern):
    table = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = table[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        table[i] = k
    return table


def kmp_search(text, pattern):
    table = prefix_table(pattern)
    found, checks, k = [], 0, 0            # k: şu an eşleşen harf sayısı
    for i, ch in enumerate(text):
        while k > 0 and ch != pattern[k]:
            checks += 1
            k = table[k - 1]               # geri çekil, metinde değil kalıpta
        checks += 1
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            found.append(i - k + 1)
            k = table[k - 1]
    return found, checks


print(prefix_table("abacab"))
print(kmp_search("abracadabra", "abra"))
```

```text
[0, 0, 1, 0, 1, 2]
([0, 7], 13)
```

Aynı eşleşmeler, 13 karşılaştırma. Fark kötü durumda ortaya çıkıyor: on bin
`a` ve bir `b` içinde elli `a` ve bir `b` arayalım.

```python
text = "a" * 10_000 + "b"
pattern = "a" * 50 + "b"
print(naive_search(text, pattern)[1], kmp_search(text, pattern)[1])
```

```text
507501 19951
```

Saf arama yarım milyondan fazla karşılaştırma yaptı, KMP yaklaşık yirmi bin:
`O(n + m)`, her metin harfi için en fazla iki karşılaştırma.

## Rabin-Karp: pencerenin parmak izi

**Rabin-Karp** her pencerenin harflerini tek tek karşılaştırmak yerine bir
**hash** (parmak izi) hesaplar. Pencere bir harf kayınca hash baştan
hesaplanmaz: çıkan harfin katkısı çıkarılır, giren harfinki eklenir
(**kayan hash, rolling hash**). Hash'ler eşitse harfler yine de kontrol edilir,
çünkü iki farklı metnin hash'i nadiren de olsa çakışabilir.

```python
def rabin_karp(text, pattern, base=256, mod=1_000_000_007):
    m = len(pattern)
    if m > len(text):
        return []
    high = pow(base, m - 1, mod)           # çıkan harfin ağırlığı
    target = window = 0
    for i in range(m):
        target = (target * base + ord(pattern[i])) % mod
        window = (window * base + ord(text[i])) % mod
    found = []
    for i in range(len(text) - m + 1):
        if window == target and text[i:i + m] == pattern:
            found.append(i)
        if i + m < len(text):
            window = (window - ord(text[i]) * high) % mod
            window = (window * base + ord(text[i + m])) % mod
    return found


print(rabin_karp("abracadabra", "abra"))
```

```text
[0, 7]
```

Rabin-Karp'ın asıl gücü **çok kalıp** ve **kopya bulma**: bütün kalıpların
hash'leri bir kümeye konur, her pencerenin hash'i kümede aranır. İntihal
denetimi ve aynı paragrafı içeren belgeleri bulmak bu fikirle çalışır.

## Trie: önek ağacı

Arama kutusu "dat" yazınca `data`, `database`, `dataset`, `date` önerir. Her
kelimeyi tek tek `startswith` ile denemek kelime sayısıyla büyür. **Trie (önek
ağacı)** kelimeleri harf harf bir ağaca koyar: ortak önekler bir kez saklanır,
önekteki düğüme inmek önek uzunluğu kadar adımdır.

<figure class="fig">
<svg viewBox="0 0 224 312" width="224" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="54.3" y1="182.0" x2="25.3" y2="236.0"/>
<line class="line" x1="83.3" y1="236.0" x2="83.3" y2="290.0"/>
<line class="line" x1="54.3" y1="182.0" x2="83.3" y2="236.0"/>
<line class="line" x1="97.8" y1="128.0" x2="54.3" y2="182.0"/>
<line class="line" x1="141.3" y1="182.0" x2="141.3" y2="236.0"/>
<line class="line" x1="97.8" y1="128.0" x2="141.3" y2="182.0"/>
<line class="line" x1="97.8" y1="74.0" x2="97.8" y2="128.0"/>
<line class="line" x1="148.6" y1="20.0" x2="97.8" y2="74.0"/>
<line class="line" x1="199.3" y1="182.0" x2="199.3" y2="236.0"/>
<line class="line" x1="199.3" y1="128.0" x2="199.3" y2="182.0"/>
<line class="line" x1="199.3" y1="74.0" x2="199.3" y2="128.0"/>
<line class="line" x1="148.6" y1="20.0" x2="199.3" y2="74.0"/>
<rect class="box" x="129.2" y="6.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="148.6" y="24.6" font-size="13" text-anchor="middle">kök</text>
<rect class="box" x="86.0" y="60.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="97.8" y="78.5" font-size="13" text-anchor="middle">c</text>
<rect class="box" x="86.0" y="114.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="97.8" y="132.6" font-size="13" text-anchor="middle">a</text>
<rect class="box" x="42.5" y="168.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="54.3" y="186.6" font-size="13" text-anchor="middle">r</text>
<rect class="box" x="13.5" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="25.3" y="240.6" font-size="13" text-anchor="middle">✓</text>
<rect class="box" x="71.5" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="83.3" y="240.6" font-size="13" text-anchor="middle">t</text>
<rect class="box" x="71.5" y="276.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="83.3" y="294.6" font-size="13" text-anchor="middle">✓</text>
<rect class="box" x="129.5" y="168.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="141.3" y="186.6" font-size="13" text-anchor="middle">t</text>
<rect class="box" x="129.5" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="141.3" y="240.6" font-size="13" text-anchor="middle">✓</text>
<rect class="box" x="187.5" y="60.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="199.3" y="78.5" font-size="13" text-anchor="middle">d</text>
<rect class="box" x="187.5" y="114.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="199.3" y="132.6" font-size="13" text-anchor="middle">o</text>
<rect class="box" x="187.5" y="168.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="199.3" y="186.6" font-size="13" text-anchor="middle">g</text>
<rect class="box" x="187.5" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="199.3" y="240.6" font-size="13" text-anchor="middle">✓</text>
</svg>
<figcaption><code>car</code>, <code>cart</code>, <code>cat</code>, <code>dog</code> içeren bir trie. <code>ca</code> öneki bir kez saklanıyor; ✓ bir kelimenin bittiği yer (kodda <code>'$'</code> anahtarı).</figcaption>
</figure>

```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True                   # burada bir kelime bitiyor

    def complete(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return []
            node = node[ch]
        words, stack = [], [(node, prefix)]
        while stack:
            node, word = stack.pop()
            for ch, child in node.items():
                if ch == "$":
                    words.append(word)
                else:
                    stack.append((child, word + ch))
        return sorted(words)


trie = Trie()
for w in ["data", "database", "date", "dataset", "deep", "model"]:
    trie.insert(w)
print(trie.complete("dat"))
print(trie.complete("x"))
```

```text
['data', 'database', 'dataset', 'date']
[]
```

## Makine öğrenmesinde

- **Tokenizasyon:** dil modellerinin sözlüğünde en uzun eşleşen parçayı bulmak
  bir önek sorusudur; trie bunun için doğal yapı.
- **Kopya ve benzer belge:** eğitim verisindeki tekrarlanan parçaları bulmak
  için kayan hash ile parça (n-gram) parmak izleri; bölüm 13'teki MinHash bunu
  büyütür.
- **Yazım düzeltme:** sözlükteki adaylar trie ile daraltılır, aralarından
  düzenleme uzaklığı (DP 2) en küçük olan seçilir.

## Özet

- Saf arama `O(n · m)`; kötü durumda yavaş.
- KMP: önek tablosu ile metinde geri dönmeden `O(n + m)`.
- Rabin-Karp: kayan hash; çok kalıp ve kopya bulmada güçlü, eşit hash'te harf
  kontrolü şart.
- Trie: ortak önekleri paylaşan ağaç; otomatik tamamlama ve sözlük araması.
