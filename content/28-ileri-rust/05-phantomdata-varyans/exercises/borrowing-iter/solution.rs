use std::marker::PhantomData;

struct Iter<'a, T> {
    ptr: *const T,
    left: usize,
    _borrow: PhantomData<&'a T>,
}

fn iter_of<T>(list: &[T]) -> Iter<'_, T> {
    Iter { ptr: list.as_ptr(), left: list.len(), _borrow: PhantomData }
}

impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<&'a T> {
        if self.left == 0 {
            return None;
        }
        // SAFETY: left items remain from ptr, and the list is borrowed for 'a.
        let item = unsafe { &*self.ptr };
        self.ptr = unsafe { self.ptr.add(1) };
        self.left -= 1;
        Some(item)
    }
}

fn main() {
    let list = [1, 2];
    println!("{}", iter_of(&list).count());
}
