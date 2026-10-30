## Try another way first

`Rc<RefCell<T>>` is used often out of habits from other languages, but in Rust it is usually not needed.

| Instead | When |
|---|---|
| Lend it (`&T`) | If the value stays in the caller's hands |
| Pass ownership | If the finished side is done giving |
| Use an index | Graphs and trees: `Vec<Node>` and `usize` |
| `clone` | If the data is small |

## An indexed graph

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

No cycle problem, no `RefCell`, no borrow clash. The price: a deleted node's index may look valid.

## A changeable closed area

A legitimate use of `RefCell`: a type that shows `&self` outside but keeps a cache or a counter inside.

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

It looks like reading from outside; the user does not want `mut`.

## Keep the locked area short

The guard returned from `borrow_mut()` holds the lock until the end of its scope. Narrowing the block prevents a panic:

```rust
{
    let mut list = shared.borrow_mut();
    list.push(1);
}
println!("{:?}", shared.borrow());
```
