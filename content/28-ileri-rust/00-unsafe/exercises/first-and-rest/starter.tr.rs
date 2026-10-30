use std::slice;

// fn first_and_rest(list: &mut [i32]) -> Option<(&mut i32, &mut [i32])> ...

fn main() {
    let mut list = [1, 2, 3];
    if let Some((first, rest)) = first_and_rest(&mut list) {
        *first = 10;
        rest[0] = 20;
    }
    println!("{list:?}");
}
