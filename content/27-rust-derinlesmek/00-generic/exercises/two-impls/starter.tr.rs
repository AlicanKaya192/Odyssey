// struct Pair ...

fn main() {
    let p = Pair { first: 1, second: 2 };
    println!("{}", p.bigger());
    println!("{:?}", p.swapped());
}
