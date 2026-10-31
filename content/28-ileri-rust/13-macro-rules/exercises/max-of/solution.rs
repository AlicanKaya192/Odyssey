macro_rules! max_of {
    ($x:expr) => {
        $x
    };
    ($x:expr, $($rest:expr),+) => {{
        let first = $x;
        let other = max_of!($($rest),+);
        if first > other { first } else { other }
    }};
}

fn main() {
    println!("{}", max_of!(4));
    println!("{}", max_of!(1, 9, 3));
}
