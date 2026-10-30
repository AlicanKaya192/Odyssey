struct Undo<'a> {
    list: &'a mut Vec<String>,
    keep: usize,
}

impl Drop for Undo<'_> {
    fn drop(&mut self) {
        self.list.truncate(self.keep);
    }
}

fn add_all(list: &mut Vec<String>, items: &[&str]) -> Result<(), String> {
    let keep = list.len();
    let undo = Undo { list, keep };
    for item in items {
        if item.is_empty() {
            return Err(String::from("empty item"));
        }
        undo.list.push(item.to_string());
    }
    std::mem::forget(undo);
    Ok(())
}

fn main() {
    let mut list = vec![String::from("a")];
    println!("{:?}", add_all(&mut list, &["b", ""]));
    println!("{list:?}");
}
