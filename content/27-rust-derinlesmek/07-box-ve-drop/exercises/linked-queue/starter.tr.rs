#[derive(Debug)]
struct Queue {
    head: Option<Box<Item>>,
}

#[derive(Debug)]
struct Item {
    value: i32,
    next: Option<Box<Item>>,
}

// impl Queue ...

fn main() {
    let mut q = Queue::new();
    q.push_front(1);
    q.push_front(2);
    println!("{:?}", q.pop_front());
}
