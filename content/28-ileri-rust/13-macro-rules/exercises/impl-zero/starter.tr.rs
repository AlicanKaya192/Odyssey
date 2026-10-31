trait Zero {
    fn zero() -> Self;
}

// macro_rules! impl_zero ...

impl_zero!(i32 => 0, f64 => 0.0, String => String::new());

fn main() {
    println!("{} {} {:?}", i32::zero(), f64::zero(), String::zero());
}
