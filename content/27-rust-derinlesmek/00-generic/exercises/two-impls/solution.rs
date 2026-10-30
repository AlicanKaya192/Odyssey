#[derive(Debug)]
struct Pair<T> {
    first: T,
    second: T,
}

impl<T> Pair<T> {
    fn swapped(self) -> Pair<T> {
        Pair { first: self.second, second: self.first }
    }
}

impl<T: PartialOrd + Copy> Pair<T> {
    fn bigger(&self) -> T {
        if self.first > self.second {
            self.first
        } else {
            self.second
        }
    }
}

fn main() {
    let p = Pair { first: 1, second: 2 };
    println!("{}", p.bigger());
    println!("{:?}", p.swapped());
}
