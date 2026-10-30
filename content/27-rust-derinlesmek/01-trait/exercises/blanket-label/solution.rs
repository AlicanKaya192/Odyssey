use std::fmt::Debug;

trait Label {
    fn label(&self) -> String;
}

impl<T: Debug> Label for T {
    fn label(&self) -> String {
        format!("<{:?}>", self)
    }
}

fn main() {
    println!("{}", 5.label());
    println!("{}", "hi".label());
}
