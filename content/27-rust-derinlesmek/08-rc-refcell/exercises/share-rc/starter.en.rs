use std::rc::Rc;

// fn share ...

fn main() {
    let a = Rc::new(String::from("x"));
    let list = share(&a, 2);
    println!("{} {}", list.len(), Rc::strong_count(&a));
}
