use std::cell::RefCell;
use std::rc::Rc;

// struct Member ...

fn main() {
    let board = Rc::new(RefCell::new(Vec::new()));
    let a = Member { board: Rc::clone(&board) };
    let b = Member { board: Rc::clone(&board) };
    a.post("hi");
    b.post("yo");
    println!("{:?}", board.borrow());
}
