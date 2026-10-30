## Yazımlar

| İş | Yazım |
|---|---|
| Sahipli | `Box<dyn Shape>` |
| Ödünç | `&dyn Shape`, `&mut dyn Shape` |
| Liste | `Vec<Box<dyn Shape>>` |
| Paylaşılan | `Rc<dyn Shape>` |
| Parametre | `fn f(s: &dyn Shape)` |
| Döndür | `fn f() -> Box<dyn Shape>` |
| Çok kısıt | `Box<dyn Shape + Send>` |
| Ömürlü | `Box<dyn Shape + 'a>` |

## Döndürme örneği

Önceki bölümde `-> impl Trait` iki tür döndüremiyordu. `Box<dyn>` yapabilir:

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

fn make(kind: &str) -> Box<dyn Shape> {
    if kind == "circle" {
        Box::new(Circle { r: 1.0 })
    } else {
        Box::new(Square { side: 1.0 })
    }
}

fn main() {
    println!("{}", make("circle").name());
    println!("{}", make("x").name());
}
```

```text
circle
square
```

## Closure da nesne olabilir

```rust
fn main() {
    let offset = 10;
    let steps: Vec<Box<dyn Fn(i32) -> i32>> = vec![
        Box::new(|x| x + 1),
        Box::new(|x| x * 2),
        Box::new(move |x| x + offset),
    ];
    let mut value = 1;
    for step in &steps {
        value = step(value);
    }
    println!("{value}");
}
```

```text
14
```

Farklı closure'ların türü farklıdır; listeye ancak böyle girerler.

## Hatalar

| Kod | Anlamı | Çözüm |
|---|---|---|
| `E0038` | Trait nesne olamaz | `-> Self` ya da generic metodu kaldır |
| `E0277` | `dyn T` boyutu bilinmiyor | `Box` ya da `&` arkasına al |
| `E0782` | `dyn` yazılmamış | `dyn` ekle |
