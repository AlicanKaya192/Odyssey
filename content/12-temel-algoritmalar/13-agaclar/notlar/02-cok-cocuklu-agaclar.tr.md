Klasörler, JSON belgeleri, bir menünün alt menüleri: gerçek hayattaki
ağaçların çoğu ikili değil, bir düğümün **istediği kadar** çocuğu var. Tek
fark, `left` ve `right` yerine bir **çocuk listesi** tutmak. İskelet aynı:
taban durumu ve çocukların cevaplarını birleştirmek.

```python
folders = {"name": "project", "size": 2, "children": [
    {"name": "data", "size": 120, "children": [
        {"name": "raw", "size": 300, "children": []}]},
    {"name": "src", "size": 15, "children": []},
]}

def total_size(folder):                       # postorder: önce çocuklar
    return folder["size"] + sum(total_size(c) for c in folder["children"])

def show(folder, depth=0):                    # preorder: önce kendisi
    print("    " * depth + folder["name"], total_size(folder))
    for child in folder["children"]:
        show(child, depth + 1)

show(folders)
```

```text
project 437
    data 420
        raw 300
    src 15
```

Burada çocuk listesi boşsa döngü hiç dönmüyor; ayrı bir `if` gerekmiyor.
Taban durumu, çocuğu olmayan düğüm.

Bir dikkat: `show` her düğümde `total_size`'ı yeniden çağırıyor, alt ağaçlar
tekrar tekrar geziliyor. Ağaç büyükse önce boyutları bir kez hesaplayıp
saklamak (ya da postorder'da tek geçişte ikisini birden yapmak) daha iyi.

## İç içe listenin derinliği

İç içe Python listesi de bir ağaç: her liste bir düğüm, içindeki listeler
çocukları.

```python
def depth(item):
    if not isinstance(item, list):
        return 0
    return 1 + max((depth(x) for x in item), default=0)

print(depth([1, [2, [3, 4]], [5]]), depth([]), depth(7))
```

```text
3 1 0
```

`max`'in `default=0`'ı boş liste için: içi boş bir listenin derinliği 1.
