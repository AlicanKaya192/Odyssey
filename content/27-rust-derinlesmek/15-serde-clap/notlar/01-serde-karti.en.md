## Basic operations

| Written as | What it does |
|---|---|
| `serde_json::to_string(&x)` | One line of JSON text |
| `serde_json::to_string_pretty(&x)` | Indented JSON text |
| `serde_json::from_str::<T>(s)` | A `T` from text |
| `serde_json::json!({...})` | Builds a `Value` in code |

## Field attributes

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    #[serde(rename = "userName")]
    name: String,
    #[serde(default = "default_lang")]
    lang: String,
    #[serde(skip)]
    cache: u32,
    #[serde(alias = "mail")]
    email: Option<String>,
}

fn default_lang() -> String {
    "en".to_string()
}

fn main() {
    let text = r#"{"userName": "Ada", "mail": "a@b.c"}"#;
    let user: User = serde_json::from_str(text).unwrap();
    println!("{user:?}");
    println!("{}", serde_json::to_string(&user).unwrap());
}
```

```text
User { name: "Ada", lang: "en", cache: 0, email: Some("a@b.c") }
{"userName":"Ada","lang":"en","email":"a@b.c"}
```

| Attribute | What it does |
|---|---|
| `rename = "userName"` | This field's name in the JSON |
| `default = "fn_name"` | If missing, this function's value |
| `skip` | Never write, never read; the default on reading |
| `alias = "mail"` | Also accept this name on reading |

## Extra fields

Extra fields are ignored by default. In settings files where you want to catch typos, use `deny_unknown_fields`:

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Strict {
    id: u32,
}

#[derive(Debug, Deserialize)]
struct Loose {
    id: u32,
}

fn main() {
    let text = r#"{"id": 1, "extra": true}"#;
    println!("{:?}", serde_json::from_str::<Loose>(text).unwrap());
    println!("{}", serde_json::from_str::<Strict>(text).unwrap_err());
}
```

```text
Loose { id: 1 }
unknown field `extra`, expected `id` at line 1 column 17
```

## Which type?

| JSON | Rust |
|---|---|
| `"text"` | `String` |
| `1` | `i32`, `u32`, `i64`... |
| `1.5` | `f64` |
| `true` | `bool` |
| `null` or missing | `Option<T>` |
| `[1, 2]` | `Vec<T>` |
| `{...}` | A struct or `HashMap<String, T>` |
