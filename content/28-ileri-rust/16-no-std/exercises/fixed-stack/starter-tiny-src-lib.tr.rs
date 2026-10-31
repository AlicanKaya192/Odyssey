#![no_std]

pub struct Stack<T, const N: usize> {
    items: [Option<T>; N],
    len: usize,
}

impl<T, const N: usize> Stack<T, N> {
    pub fn new() -> Self {
        Stack { items: [const { None }; N], len: 0 }
    }

    // pub fn push(&mut self, value: T) -> Result<(), T> ...
    // pub fn pop(&mut self) -> Option<T> ...
}
