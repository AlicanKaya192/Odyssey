// struct Highlight ...

fn main() {
    let h = Highlight { text: "hello world", start: 6, end: 11 };
    println!("{} {}", h.part(), h.len());
}
