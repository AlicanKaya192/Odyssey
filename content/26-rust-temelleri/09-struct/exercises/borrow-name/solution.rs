struct Person {
    name: String,
}

impl Person {
    fn name(&self) -> &str {
        &self.name
    }

    fn into_name(self) -> String {
        self.name
    }
}

fn main() {
    let p = Person { name: String::from("Ada") };
    println!("{}", p.name());
    let owned = p.into_name();
    println!("{owned}");
}
