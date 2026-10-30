use std::cell::RefCell;
use std::rc::Rc;

struct Member {
    board: Rc<RefCell<Vec<String>>>,
}

impl Member {
    fn post(&self, text: &str) {
        self.board.borrow_mut().push(text.to_string());
    }
}

fn main() {
    let board = Rc::new(RefCell::new(Vec::new()));
    let a = Member { board: Rc::clone(&board) };
    let b = Member { board: Rc::clone(&board) };
    a.post("hi");
    b.post("yo");
    println!("{:?}", board.borrow());
}
