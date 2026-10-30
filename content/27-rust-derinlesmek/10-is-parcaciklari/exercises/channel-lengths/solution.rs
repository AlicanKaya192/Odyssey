use std::sync::mpsc;
use std::thread;

fn lengths(words: Vec<String>) -> Vec<usize> {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        for w in words {
            tx.send(w.len()).unwrap();
        }
    });
    rx.iter().collect()
}

fn main() {
    println!("{:?}", lengths(vec![String::from("go"), String::from("rust")]));
}
