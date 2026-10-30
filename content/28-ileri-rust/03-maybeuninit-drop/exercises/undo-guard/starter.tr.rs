struct Undo<'a> {
    list: &'a mut Vec<String>,
    keep: usize,
}

// impl Drop for Undo<'_> ...

// fn add_all(list: &mut Vec<String>, items: &[&str]) -> Result<(), String> ...

fn main() {
    let mut list = vec![String::from("a")];
    println!("{:?}", add_all(&mut list, &["b", ""]));
    println!("{list:?}");
}
