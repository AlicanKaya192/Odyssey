enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

fn sum(list: &List) -> i32 {
    match list {
        Cons(value, rest) => value + sum(rest),
        Nil => 0,
    }
}

fn len(list: &List) -> usize {
    match list {
        Cons(_, rest) => 1 + len(rest),
        Nil => 0,
    }
}

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Nil))));
    println!("{} {}", sum(&list), len(&list));
}
