fn append_longer(target: &mut String, a: &String, b: &String) {
    if b.len() > a.len() {
        target.push_str(b);
    } else {
        target.push_str(a);
    }
}

fn main() {
    let mut out = String::from("> ");
    let a = String::from("short");
    let b = String::from("longer one");
    append_longer(&mut out, &a, &b);
    println!("{out} ({a}, {b})");
}
