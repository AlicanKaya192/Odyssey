Birleşim-bulma yalnızca Kruskal için değil. Kenarlar **teker teker
geldiğinde** "kaç grup var?" ve "bu kenar döngü kurdu mu?" sorularını her
seferinde grafı baştan gezmeden cevaplar.

```python
parent = list(range(6))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

groups = 6
for a, b in [(0, 1), (2, 3), (1, 2), (4, 5), (0, 3)]:
    ra, rb = find(a), find(b)
    if ra == rb:
        print(a, b, "-> cycle!")
    else:
        parent[ra] = rb
        groups -= 1
        print(a, b, "-> groups:", groups)
```

```text
0 1 -> groups: 5
2 3 -> groups: 4
1 2 -> groups: 3
4 5 -> groups: 2
0 3 -> cycle!
```

Her yeni bağlantı iki grubu birleştiriyorsa grup sayısı bir azalır; `0`–`3`
geldiğinde ikisi zaten aynı gruptaydı, yani bu kenar bir döngü kapattı. BFS
ile aynı soruları her kenarda baştan sormak `O(n + m)`, burada her kenar
pratikte sabit süre.

Aynı kalıbın kullanıldığı yerler: sosyal ağda arkadaş çevreleri, bir haritada
adalar, aynı kişiye ait hesapları (ortak e-posta ya da telefon) birleştirmek,
kayıt eşleştirmede (entity resolution) "aynı varlık" gruplarını kurmak.
