use std::marker::PhantomData;

struct User;

struct Id<T> {
    value: u32,
    _marker: PhantomData<fn() -> T>,
}

impl<T> Id<T> {
    fn new(value: u32) -> Self {
        Id { value, _marker: PhantomData }
    }

    fn value(&self) -> u32 {
        self.value
    }
}

fn main() {
    let id: Id<User> = Id::new(3);
    println!("{}", id.value());
}
