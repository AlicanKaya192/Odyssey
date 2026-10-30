// fn append_longer ...

fn main() {
    let mut out = String::from("> ");
    let a = String::from("short");
    let b = String::from("longer one");
    append_longer(&mut out, &a, &b);
    println!("{out} ({a}, {b})");
}
