#[derive(Debug)]
struct Stack {
    items: Vec<i32>,
}

impl Stack {
    fn new() -> Stack {
        Stack { items: Vec::new() }
    }

    fn push(&mut self, value: i32) {
        self.items.push(value);
    }

    fn pop(&mut self) -> Option<i32> {
        self.items.pop()
    }

    fn peek(&self) -> Option<&i32> {
        self.items.last()
    }

    fn len(&self) -> usize {
        self.items.len()
    }
}

fn main() {
    let mut s = Stack::new();
    s.push(1);
    println!("{:?} {:?}", s.peek(), s.len());
}
