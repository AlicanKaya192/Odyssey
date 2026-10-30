#[derive(Debug, PartialEq)]
struct Meters(f64);

struct Kilometers(f64);

impl From<Kilometers> for Meters {
    fn from(k: Kilometers) -> Meters {
        Meters(k.0 * 1000.0)
    }
}

fn main() {
    let m: Meters = Kilometers(1.5).into();
    println!("{:?}", m);
}
