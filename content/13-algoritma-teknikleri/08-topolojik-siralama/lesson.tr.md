# Topolojik Sıralama

Bir veri hattında işlerin sırası önemli: veriyi çekmeden temizleyemezsin,
özellikleri çıkarmadan model eğitemezsin. "`clean`, `extract`'tan sonra
gelmeli" gibi kurallar **yönlü** bir graftır: ok, "önce bu, sonra o" der.
**Topolojik sıralama (topological sort)** bütün okların ileri baktığı bir
iş sırası bulur.

<figure class="fig">
<svg viewBox="0 0 770 260" width="770" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dim" d="M0 0L10 5L0 10z"/></marker></defs>
<line class="line" x1="79.5" y1="113.1" x2="158.7" y2="67.9" marker-end="url(#arr)"/>
<line class="line" x1="79.5" y1="146.9" x2="158.7" y2="192.1" marker-end="url(#arr)"/>
<line class="line" x1="219.5" y1="66.9" x2="298.7" y2="112.1" marker-end="url(#arr)"/>
<line class="line" x1="219.5" y1="193.1" x2="298.7" y2="147.9" marker-end="url(#arr)"/>
<line class="line" x1="364.0" y1="130.0" x2="424.0" y2="130.0" marker-end="url(#arr)"/>
<line class="line" x1="494.0" y1="130.0" x2="554.0" y2="130.0" marker-end="url(#arr)"/>
<line class="line" x1="619.0" y1="112.2" x2="689.3" y2="68.9" marker-end="url(#arr)"/>
<line class="line" x1="224.0" y1="50.0" x2="684.0" y2="50.0" marker-end="url(#arr)"/>
<circle class="box" cx="50" cy="130" r="34"/>
<text class="ink" x="50" y="133.8" font-size="11" text-anchor="middle">extract</text>
<circle class="box" cx="190" cy="50" r="34"/>
<text class="ink" x="190" y="53.9" font-size="11" text-anchor="middle">clean</text>
<circle class="box" cx="190" cy="210" r="34"/>
<text class="ink" x="190" y="213.8" font-size="11" text-anchor="middle">validate</text>
<circle class="box" cx="330" cy="130" r="34"/>
<text class="ink" x="330" y="133.8" font-size="11" text-anchor="middle">features</text>
<circle class="box" cx="460" cy="130" r="34"/>
<text class="ink" x="460" y="133.8" font-size="11" text-anchor="middle">train</text>
<circle class="box" cx="590" cy="130" r="34"/>
<text class="ink" x="590" y="133.8" font-size="11" text-anchor="middle">evaluate</text>
<circle class="box" cx="720" cy="50" r="34"/>
<text class="ink" x="720" y="53.9" font-size="11" text-anchor="middle">report</text>
</svg>
<figcaption>Bir veri hattı: her ok "önce bu, sonra o" diyor. Yönlü döngü yok; bu bir DAG.</figcaption>
</figure>

Böyle bir sıra ancak grafta **yönlü döngü yoksa** vardır: `A`, `B`'den önce
ve `B`, `A`'dan önce olamaz. Döngüsüz yönlü grafa **DAG (directed acyclic
graph)** denir. Ders ön koşulları, derleme sistemleri (`make`), tablo
formüllerinin hesap sırası ve Airflow gibi veri hattı araçları DAG'dir.

## Kahn algoritması: önce bekleyeni olmayan

Her işin kaç işi **beklediğini** (giren derece) say. Beklediği iş kalmayan
işleri yap; yaptığın işin arkasındakilerin sayacını bir azalt, sıfıra inen
yeni işleri sıraya ekle.

```python
import heapq

deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}

def kahn(deps):
    nodes = set(deps) | {d for needs in deps.values() for d in needs}
    after = {n: [] for n in nodes}
    waiting = {n: 0 for n in nodes}          # kaç işi bekliyor
    for task, needs in deps.items():
        for need in needs:
            after[need].append(task)
            waiting[task] += 1
    ready = [n for n in nodes if waiting[n] == 0]
    heapq.heapify(ready)                     # eşitlikte alfabetik
    order = []
    while ready:
        task = heapq.heappop(ready)
        order.append(task)
        for nxt in after[task]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                heapq.heappush(ready, nxt)
    return order if len(order) == len(nodes) else None   # eksikse döngü var

print(kahn(deps))
cyclic = dict(deps, extract=["report"])     # report → extract: döngü
print(kahn(cyclic))
```

```text
['extract', 'clean', 'validate', 'features', 'train', 'evaluate', 'report']
None
```

Döngülü grafta hiçbir işin bekleyeni sıfıra inmiyor; sıra yarıda kalıyor ve
bu, döngünün kendisini **teşhis** ediyor. Her düğüm ve kenar bir kez:
`O(n + m)`. Hazır heap yerine sıradan bir kuyruk da olur; heap yalnızca
eşitlikte alfabetik sırayı garanti etmek için.

## DFS ile: önce bağımlılıkları bitir

Bir işi yapmadan önce bütün bağımlılıklarını (özyinelemeyle) bitir, sonra işi
listeye ekle. Döngüyü yakalamak için her düğümün üç durumu var: hiç
görülmedi, **şu an yığında** (`active`), bitti (`done`). Yığındaki bir düğüme
yeniden gelinirse döngü vardır.

```python
def dfs_order(deps):
    nodes = sorted(set(deps) | {d for needs in deps.values() for d in needs})
    state, order = {}, []
    def visit(task):
        if state.get(task) == "done":
            return True
        if state.get(task) == "active":       # kendi yolunda yeniden: döngü
            return False
        state[task] = "active"
        for need in sorted(deps.get(task, [])):
            if not visit(need):
                return False
        state[task] = "done"
        order.append(task)                    # bağımlılıklar bitti
        return True
    for task in nodes:
        if not visit(task):
            return None
    return order

print(dfs_order(deps), dfs_order(cyclic))
```

```text
['extract', 'clean', 'validate', 'features', 'train', 'evaluate', 'report'] None
```

## Hazırı: `graphlib`

Python'un standart kütüphanesinde `graphlib.TopologicalSorter` var; döngüyü
de hatayla bildirir ve döngünün kendisini gösterir:

```python
from graphlib import TopologicalSorter, CycleError

print(list(TopologicalSorter(deps).static_order()))
try:
    list(TopologicalSorter(cyclic).static_order())
except CycleError as error:
    print("cycle:", error.args[1])
```

```text
['extract', 'clean', 'validate', 'features', 'train', 'evaluate', 'report']
cycle: ['clean', 'features', 'train', 'evaluate', 'report', 'extract', 'clean']
```

## Kritik yol: hat en erken ne zaman biter?

Her işin bir süresi varsa ve birbirini beklemeyen işler aynı anda
yapılabiliyorsa, hattın bitiş süresi **en uzun bağımlılık zincirinin**
toplamıdır. Topolojik sırayla tek geçiş yeter: bir işin bitişi, kendi süresi
+ bağımlılıklarının en geç bitişi.

```python
hours = {"extract": 2, "clean": 3, "validate": 1, "features": 4,
         "train": 6, "evaluate": 1, "report": 2}
finish = {}
for task in kahn(deps):
    finish[task] = hours[task] + max((finish[d] for d in deps.get(task, [])), default=0)
for task, t in finish.items():
    print(task, t)
print("pipeline done after", max(finish.values()), "hours")
```

```text
extract 2
clean 5
validate 3
features 9
train 15
evaluate 16
report 18
pipeline done after 18 hours
```

Toplam iş 19 saat, ama `validate` `clean` ile aynı anda yapılabildiği için hat
18 saatte biter. `extract → clean → features → train → evaluate → report`
**kritik yol**: bunlardan birindeki gecikme bütün hattı geciktirir. Proje
yönetimindeki kritik yol yöntemi (CPM) de budur.

## Özet

- Topolojik sıralama: bütün okların ileri baktığı sıra; yalnızca DAG'de var.
- Kahn: bekleyeni olmayanı al, arkasındakilerin sayacını azalt; eksik kalırsa
  döngü.
- DFS: önce bağımlılıklar; `active` düğüme yeniden gelmek döngü.
- `graphlib.TopologicalSorter`: hazırı, `CycleError` ile.
- Kritik yol: topolojik sırayla bitiş süreleri; en uzun zincir.
- Hepsi `O(n + m)`.
