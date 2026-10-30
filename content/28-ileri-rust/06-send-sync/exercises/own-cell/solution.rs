use std::cell::UnsafeCell;

struct MyCell<T> {
    value: UnsafeCell<T>,
}

impl<T: Copy> MyCell<T> {
    fn new(value: T) -> Self {
        MyCell { value: UnsafeCell::new(value) }
    }

    fn get(&self) -> T {
        // SAFETY: MyCell is not Sync and gives no references.
        unsafe { *self.value.get() }
    }

    fn set(&self, value: T) {
        // SAFETY: as above.
        unsafe { *self.value.get() = value };
    }

    fn update(&self, change: impl Fn(T) -> T) {
        self.set(change(self.get()));
    }
}

fn main() {
    let c = MyCell::new(1);
    c.update(|n| n + 1);
    println!("{}", c.get());
}
