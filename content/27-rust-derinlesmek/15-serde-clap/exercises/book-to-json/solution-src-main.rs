use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Book {
    title: String,
    pages: u32,
}

fn main() {
    let book = Book { title: "Dune".to_string(), pages: 412 };
    println!("{}", serde_json::to_string(&book).unwrap());
}
