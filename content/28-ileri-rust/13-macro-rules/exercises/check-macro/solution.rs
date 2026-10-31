macro_rules! check {
    ($x:expr) => {
        if $x {
            Ok(())
        } else {
            Err(format!("failed: {}", stringify!($x)))
        }
    };
}

fn main() {
    println!("{:?}", check!(1 + 1 == 2));
    println!("{:?}", check!(1 + 1 == 3));
}
