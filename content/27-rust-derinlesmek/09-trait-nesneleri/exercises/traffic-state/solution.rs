trait Light {
    fn next(self: Box<Self>) -> Box<dyn Light>;
    fn color(&self) -> String;
}

struct Red;
struct Green;

impl Light for Red {
    fn next(self: Box<Self>) -> Box<dyn Light> {
        Box::new(Green)
    }

    fn color(&self) -> String {
        String::from("red")
    }
}

impl Light for Green {
    fn next(self: Box<Self>) -> Box<dyn Light> {
        Box::new(Red)
    }

    fn color(&self) -> String {
        String::from("green")
    }
}

fn main() {
    let mut l: Box<dyn Light> = Box::new(Red);
    l = l.next();
    println!("{}", l.color());
}
