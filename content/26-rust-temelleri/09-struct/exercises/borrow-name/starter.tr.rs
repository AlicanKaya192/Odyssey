struct Person {
    name: String,
}

// impl Person ...

fn main() {
    let p = Person { name: String::from("Ada") };
    println!("{}", p.name());
    let owned = p.into_name();
    println!("{owned}");
}
