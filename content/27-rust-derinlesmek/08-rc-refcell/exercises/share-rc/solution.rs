use std::rc::Rc;

fn share(value: &Rc<String>, times: usize) -> Vec<Rc<String>> {
    let mut out = Vec::new();
    for _ in 0..times {
        out.push(Rc::clone(value));
    }
    out
}

fn main() {
    let a = Rc::new(String::from("x"));
    let list = share(&a, 2);
    println!("{} {}", list.len(), Rc::strong_count(&a));
}
