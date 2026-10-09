İki klasik tasarım sorusu; ikisi de mülakatlarda sık çıkar ve yığının
gücünü gösterir.

## İki yığınla kuyruk

Elinde yalnızca yığın varsa bir kuyruk kurabilir misin? Evet: biri **giriş**,
biri **çıkış** için iki yığın. Ekleme giriş yığınına gider. Alırken çıkış
yığını boşsa giriş yığınındakilerin hepsini tek tek çıkışa aktar: sıra ters
döner ve en eski eleman üste gelir.

```python
class TwoStackQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()

q = TwoStackQueue()
for x in [1, 2, 3]:
    q.push(x)
print(q.pop(), q.pop())        # 1 2
q.push(4)
print(q.pop(), q.pop())        # 3 4
```

Bir aktarma `O(n)` gibi görünür, ama her eleman ömründe **en fazla bir kez**
aktarılır: ortalamada her işlem `O(1)` (amortize).

## En küçüğü bilen yığın

Yığına ekleyip çıkarırken her an **en küçük** elemanı `O(1)`'de söyleyebilir
misin? Her elemanın yanına "bu eleman eklendiğinde yığındaki en küçük" değeri
de koy:

```python
class MinStack:
    def __init__(self):
        self.items = []                    # (değer, o andaki en küçük)

    def push(self, x):
        smallest = x if not self.items else min(x, self.items[-1][1])
        self.items.append((x, smallest))

    def pop(self):
        return self.items.pop()[0]

    def minimum(self):
        return self.items[-1][1]

s = MinStack()
for x in [5, 3, 7, 2]:
    s.push(x)
print(s.minimum())   # 2
s.pop()
print(s.minimum())   # 3
```

Üstteki eleman çıkınca altındakinin kaydettiği en küçük zaten hazır; bütün
yığını yeniden taramaya gerek yok.
