#[derive(Debug)]
struct Queue {
    head: Option<Box<Item>>,
}

#[derive(Debug)]
struct Item {
    value: i32,
    next: Option<Box<Item>>,
}

impl Queue {
    fn new() -> Queue {
        Queue { head: None }
    }

    fn push_front(&mut self, value: i32) {
        let next = self.head.take();
        self.head = Some(Box::new(Item { value, next }));
    }

    fn pop_front(&mut self) -> Option<i32> {
        let item = self.head.take()?;
        self.head = item.next;
        Some(item.value)
    }
}

fn main() {
    let mut q = Queue::new();
    q.push_front(1);
    q.push_front(2);
    println!("{:?}", q.pop_front());
}
