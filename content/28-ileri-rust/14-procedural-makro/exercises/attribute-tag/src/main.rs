use my_macros::tag;

#[tag(db)]
fn load() -> u32 {
    1
}

#[tag(net)]
fn send(n: u32) -> u32 {
    n + 1
}

fn main() {
    println!("{}", load());
    println!("{}", send(1));
}
