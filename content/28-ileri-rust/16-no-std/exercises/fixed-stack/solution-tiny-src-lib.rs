#![no_std]

pub struct Stack<T, const N: usize> {
    items: [Option<T>; N],
    len: usize,
}

impl<T, const N: usize> Stack<T, N> {
    pub fn new() -> Self {
        Stack { items: [const { None }; N], len: 0 }
    }

    pub fn push(&mut self, value: T) -> Result<(), T> {
        if self.len == N {
            return Err(value);
        }
        self.items[self.len] = Some(value);
        self.len += 1;
        Ok(())
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.len == 0 {
            return None;
        }
        self.len -= 1;
        self.items[self.len].take()
    }
}
