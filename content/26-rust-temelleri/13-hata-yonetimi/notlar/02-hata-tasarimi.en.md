## Which way to choose?

| Question | Answer |
|---|---|
| May the value really be absent? | `Option` |
| Does the reason matter? | `Result` |
| Will the caller act differently per error? | An enum error type |
| Will only a message be printed? | `Result<T, String>` is enough |
| Is this a programming bug? | `panic!` |

## A validating constructor

To make sure an invalid value can never exist, struct fields are hidden and the constructor returns `Result`. We will see hiding a field with modules in the next section; the idea is this:

```rust
#[derive(Debug)]
struct Age(u8);

impl Age {
    fn new(value: i32) -> Result<Age, String> {
        if value < 0 || value > 150 {
            return Err(format!("age must be 0-150, got {value}"));
        }
        Ok(Age(value as u8))
    }
}

fn main() {
    println!("{:?}", Age::new(36));
    println!("{:?}", Age::new(200));
}
```

```text
Ok(Age(36))
Err("age must be 0-150, got 200")
```

So the rest of the program does not keep asking "is the age valid?": if there is an `Age`, it is valid.

## A good error message

| Bad | Good |
|---|---|
| `error` | `age must be 0-150, got 200` |
| `invalid input` | `line 3: "abc" is not a number` |

What was expected, what came, and where? A message should say these three.

## Do not swallow errors

`let _ = risky();` throws away the result on purpose and silences the compiler. It is fine if you know what you are doing; as a habit, errors get lost silently.

## In the next module

`Display`, `std::error::Error`, automatic conversion with `From` (which `?` uses) and `Box<dyn Error>`.
