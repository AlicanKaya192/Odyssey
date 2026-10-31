use tiny::Stack;

fn main() {
    let mut stack = Stack::<String, 2>::new();
    println!("{:?}", stack.pop());
    println!("{:?}", stack.push(String::from("a")));
    println!("{:?}", stack.push(String::from("b")));
    println!("{:?}", stack.push(String::from("c")));
    println!("{:?}", stack.pop());
    println!("{:?}", stack.pop());
    println!("{:?}", stack.pop());
}
