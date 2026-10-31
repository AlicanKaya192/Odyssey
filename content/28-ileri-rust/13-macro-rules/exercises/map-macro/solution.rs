use std::collections::HashMap;

macro_rules! map {
    ( $( $key:expr => $value:expr ),* $(,)? ) => {{
        let mut out = HashMap::new();
        $( out.insert($key, $value); )*
        out
    }};
}

fn main() {
    let ages = map! { "ada" => 36, "alan" => 41, };
    println!("{}", ages["ada"] + ages["alan"]);
}
