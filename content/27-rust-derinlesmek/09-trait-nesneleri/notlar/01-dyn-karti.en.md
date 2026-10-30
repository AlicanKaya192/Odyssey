## Forms

| Job | Written |
|---|---|
| Owned | `Box<dyn Shape>` |
| Borrowed | `&dyn Shape`, `&mut dyn Shape` |
| A list | `Vec<Box<dyn Shape>>` |
| Shared | `Rc<dyn Shape>` |
| A parameter | `fn f(s: &dyn Shape)` |
| Return | `fn f() -> Box<dyn Shape>` |
| Several bounds | `Box<dyn Shape + Send>` |
| With a lifetime | `Box<dyn Shape + 'a>` |

## A returning example

In an earlier section `-> impl Trait` could not return two types. `Box<dyn>` can:

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

## A closure can be an object too

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

Different closures have different types; only this way can they enter a list.

## Errors

| Code | Meaning | Fix |
|---|---|---|
| `E0038` | The trait cannot be an object | Remove `-> Self` or a generic method |
| `E0277` | The size of `dyn T` is unknown | Put it behind `Box` or `&` |
| `E0782` | `dyn` was not written | Add `dyn` |
