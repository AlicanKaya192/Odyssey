use std::collections::HashMap;

// macro_rules! map ...

fn main() {
    let ages = map! { "ada" => 36, "alan" => 41, };
    println!("{}", ages["ada"] + ages["alan"]);
}
