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

fn make(kind: &str) -> Option<Box<dyn Animal>> {
    match kind {
        "dog" => Some(Box::new(Dog)),
        "cat" => Some(Box::new(Cat)),
        _ => None,
    }
}

fn main() {
    println!("{}", make("cat").map(|a| a.sound()).unwrap_or_default());
}
