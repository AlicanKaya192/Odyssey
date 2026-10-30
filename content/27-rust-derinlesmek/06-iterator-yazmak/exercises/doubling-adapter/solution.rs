struct Doubled<I> {
    inner: I,
}

impl<I: Iterator<Item = i32>> Iterator for Doubled<I> {
    type Item = i32;

    fn next(&mut self) -> Option<i32> {
        self.inner.next().map(|x| x * 2)
    }
}

fn main() {
    let d = Doubled { inner: vec![1, 2].into_iter() };
    println!("{:?}", d.collect::<Vec<i32>>());
}
