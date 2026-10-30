enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

// fn sum ...
// fn len ...

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Nil))));
    println!("{} {}", sum(&list), len(&list));
}
