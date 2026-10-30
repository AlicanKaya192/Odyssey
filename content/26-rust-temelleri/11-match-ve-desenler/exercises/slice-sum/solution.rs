fn largest(values: &[i32]) -> Option<i32> {
    match values {
        [] => None,
        [first, rest @ ..] => match largest(rest) {
            Some(best) if best > *first => Some(best),
            _ => Some(*first),
        },
    }
}

fn main() {
    println!("{:?}", largest(&[3, 9, 2]));
}
