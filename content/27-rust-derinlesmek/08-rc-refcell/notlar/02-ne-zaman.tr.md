## Önce başka yol dene

`Rc<RefCell<T>>` başka dillerin alışkanlığıyla sık kullanılır, ama Rust'ta çoğu zaman gerekmez.

| Yerine | Ne zaman |
|---|---|
| Ödünç ver (`&T`) | Değer çağıranın elinde kalıyorsa |
| Sahipliği geçir | İşi biten taraf vermeyi bitiriyorsa |
| İndeks kullan | Grafik ve ağaçlar: `Vec<Node>` ve `usize` |
| `clone` | Veri küçükse |

## İndeksli grafik

```rust
struct Graph {
    names: Vec<String>,
    edges: Vec<Vec<usize>>,
}

impl Graph {
    fn add(&mut self, name: &str) -> usize {
        self.names.push(name.to_string());
        self.edges.push(Vec::new());
        self.names.len() - 1
    }

    fn link(&mut self, from: usize, to: usize) {
        self.edges[from].push(to);
    }
}

fn main() {
    let mut g = Graph { names: Vec::new(), edges: Vec::new() };
    let a = g.add("a");
    let b = g.add("b");
    g.link(a, b);
    g.link(b, a);
    for to in &g.edges[a] {
        println!("{}", g.names[*to]);
    }
}
```

```text
b
```

Döngü sorunu yok, `RefCell` yok, ödünç çakışması yok. Bedeli: Silinmiş düğümün indeksi geçerli görünebilir.

## Değişebilir kapalı alan

`RefCell`'in meşru kullanımı: Dışarıdan `&self` görünen ama içeride önbellek ya da sayaç tutan tür.

```rust
struct Cache {
    hits: Cell<u32>,
}

impl Cache {
    fn lookup(&self) {
        self.hits.set(self.hits.get() + 1);
    }
}
```

Dışarıdan okuma gibi görünür; kullanan kişi `mut` istemez.

## Kilitli alanı kısa tut

`borrow_mut()`'tan dönen koruyucu kapsam sonuna kadar kilidi tutar. Bloğu daraltmak paniği önler:

```rust
{
    let mut list = shared.borrow_mut();
    list.push(1);
}
println!("{:?}", shared.borrow());
```
