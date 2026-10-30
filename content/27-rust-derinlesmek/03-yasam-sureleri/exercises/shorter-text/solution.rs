fn shorter<'a>(x: &'a str, y: &'a str) -> &'a str {
    if y.len() < x.len() { y } else { x }
}

fn main() {
    println!("{}", shorter("abc", "de"));
}
