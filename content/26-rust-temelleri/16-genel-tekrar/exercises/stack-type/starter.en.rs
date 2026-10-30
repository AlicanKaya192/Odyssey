// struct Stack ...

fn main() {
    let mut s = Stack::new();
    s.push(1);
    println!("{:?} {:?}", s.peek(), s.len());
}
