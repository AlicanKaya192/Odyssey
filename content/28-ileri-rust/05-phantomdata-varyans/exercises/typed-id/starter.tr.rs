use std::marker::PhantomData;

struct User;

// struct Id<T> ...
// impl<T> Id<T> { fn new(value: u32) -> Self ...  fn value(&self) -> u32 ... }

fn main() {
    let id: Id<User> = Id::new(3);
    println!("{}", id.value());
}
