use std::cell::RefCell;
use std::rc::Rc;
use std::thread;

fn count_up(n: u32) -> u32 {
    let total = Rc::new(RefCell::new(0));
    let copy = Rc::clone(&total);
    let handle = thread::spawn(move || {
        for _ in 0..n {
            *copy.borrow_mut() += 1;
        }
    });
    handle.join().unwrap();
    let result = *total.borrow();
    result
}

fn main() {
    println!("{}", count_up(5));
}
