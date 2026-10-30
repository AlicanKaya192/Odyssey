use std::thread;

fn squares(list: Vec<i32>) -> Vec<i32> {
    let handle = thread::spawn(move || {
        let mut out = Vec::new();
        for n in list {
            out.push(n * n);
        }
        out
    });
    handle.join().unwrap()
}

fn main() {
    println!("{:?}", squares(vec![1, 2, 3]));
}
