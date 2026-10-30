fn count_of<T: PartialEq, const N: usize>(items: [T; N], wanted: T) -> usize {
    let mut count = 0;
    for item in items {
        if item == wanted {
            count += 1;
        }
    }
    count
}

fn main() {
    println!("{}", count_of([1, 2, 1], 1));
}
