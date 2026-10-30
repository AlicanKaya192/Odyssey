use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    name: String,
    parent: RefCell<Weak<Node>>,
}

// fn parent_name ...

fn main() {
    let root = Rc::new(Node { name: String::from("root"), parent: RefCell::new(Weak::new()) });
    let leaf = Node { name: String::from("leaf"), parent: RefCell::new(Rc::downgrade(&root)) };
    println!("{:?} {}", parent_name(&leaf), leaf.name);
}
