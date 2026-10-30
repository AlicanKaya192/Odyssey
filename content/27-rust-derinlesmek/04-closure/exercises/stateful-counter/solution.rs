fn counter(step: u32) -> impl FnMut() -> u32 {
    let mut total = 0;
    move || {
        total += step;
        total
    }
}

fn main() {
    let mut c = counter(2);
    println!("{} {}", c(), c());
}
