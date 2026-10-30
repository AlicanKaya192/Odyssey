use std::ops::Deref;

struct Wrapper(Vec<i32>);

// impl Deref ...

fn main() {
    let w = Wrapper(vec![1, 2]);
    println!("{} {:?}", w.len(), w.first());
}
