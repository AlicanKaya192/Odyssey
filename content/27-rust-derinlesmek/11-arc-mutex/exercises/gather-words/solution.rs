use std::sync::{Arc, Mutex};
use std::thread;

fn gather(words: Vec<String>) -> Vec<String> {
    let list = Arc::new(Mutex::new(Vec::new()));
    let mut handles = Vec::new();
    for word in words {
        let list = Arc::clone(&list);
        handles.push(thread::spawn(move || {
            list.lock().unwrap().push(word.to_uppercase());
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    let mut out = list.lock().unwrap().clone();
    out.sort();
    out
}

fn main() {
    println!("{:?}", gather(vec![String::from("b"), String::from("a")]));
}
