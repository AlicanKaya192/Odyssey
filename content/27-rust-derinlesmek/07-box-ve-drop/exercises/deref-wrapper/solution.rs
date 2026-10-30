use std::ops::Deref;

struct Wrapper(Vec<i32>);

impl Deref for Wrapper {
    type Target = Vec<i32>;

    fn deref(&self) -> &Vec<i32> {
        &self.0
    }
}

fn main() {
    let w = Wrapper(vec![1, 2]);
    println!("{} {:?}", w.len(), w.first());
}
