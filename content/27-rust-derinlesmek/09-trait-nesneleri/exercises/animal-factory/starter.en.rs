trait Animal {
    fn sound(&self) -> String;
}

struct Dog;
struct Cat;

impl Animal for Dog {
    fn sound(&self) -> String {
        String::from("woof")
    }
}

impl Animal for Cat {
    fn sound(&self) -> String {
        String::from("meow")
    }
}

// fn make ...

fn main() {
    println!("{}", make("cat").map(|a| a.sound()).unwrap_or_default());
}
