// struct Counter ...
// impl Counter ...

fn main() {
    let mut c = Counter::new();
    c.increment();
    c.increment();
    println!("{}", c.value());
}
