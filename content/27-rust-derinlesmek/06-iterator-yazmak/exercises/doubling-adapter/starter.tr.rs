// struct Doubled ...

fn main() {
    let d = Doubled { inner: vec![1, 2].into_iter() };
    println!("{:?}", d.collect::<Vec<i32>>());
}
