use std::marker::PhantomData;

struct Iter<'a, T> {
    ptr: *const T,
    left: usize,
    _borrow: PhantomData<&'a T>,
}

fn iter_of<T>(list: &[T]) -> Iter<'_, T> {
    Iter { ptr: list.as_ptr(), left: list.len(), _borrow: PhantomData }
}

// impl<'a, T> Iterator for Iter<'a, T> ...

fn main() {
    let list = [1, 2];
    println!("{}", iter_of(&list).count());
}
