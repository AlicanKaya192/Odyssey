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

// fn choir ...

fn main() {
    let list: Vec<Box<dyn Animal>> = vec![Box::new(Dog), Box::new(Cat)];
    println!("{:?}", choir(&list));
}
