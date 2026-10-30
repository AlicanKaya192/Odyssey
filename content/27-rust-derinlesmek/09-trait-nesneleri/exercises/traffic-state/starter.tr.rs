// trait Light ...

fn main() {
    let mut l: Box<dyn Light> = Box::new(Red);
    l = l.next();
    println!("{}", l.color());
}
