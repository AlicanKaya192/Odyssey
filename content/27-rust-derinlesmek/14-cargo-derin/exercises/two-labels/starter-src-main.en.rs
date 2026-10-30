// fn label with #[cfg(feature = ...)]
// a second fn label with #[cfg(not(feature = ...))]

fn main() {
    println!("{}", label(10));
}
