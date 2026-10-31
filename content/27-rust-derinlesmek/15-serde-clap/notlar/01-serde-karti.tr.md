## Temel işlemler

| Yazım | Ne yapar |
|---|---|
| `serde_json::to_string(&x)` | Tek satır JSON metni |
| `serde_json::to_string_pretty(&x)` | Girintili JSON metni |
| `serde_json::from_str::<T>(s)` | Metinden `T` |
| `serde_json::json!({...})` | Kodda `Value` kurar |

## Alan öznitelikleri

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

| Öznitelik | Ne yapar |
|---|---|
| `rename = "userName"` | Bu alanın JSON'daki adı |
| `default = "fn_adı"` | Eksikse bu fonksiyonun değeri |
| `skip` | Hiç yazma, hiç okuma; okurken varsayılan |
| `alias = "mail"` | Okurken bu adı da kabul et |

## Fazladan alan

Fazladan alan varsayılan olarak yok sayılır. Yazım hatalarını yakalamak istediğin ayar dosyalarında `deny_unknown_fields` kullan:

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

## Hangi tür?

| JSON | Rust |
|---|---|
| `"text"` | `String` |
| `1` | `i32`, `u32`, `i64`... |
| `1.5` | `f64` |
| `true` | `bool` |
| `null` ya da yok | `Option<T>` |
| `[1, 2]` | `Vec<T>` |
| `{...}` | struct ya da `HashMap<String, T>` |
