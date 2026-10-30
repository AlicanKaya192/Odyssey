use std::thread;

fn main() {
    let name = String::from("Ada");
    let handle = thread::spawn(|| {
        println!("{name}");
    });
    handle.join().unwrap();
}
