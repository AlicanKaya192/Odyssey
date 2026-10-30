enum Op {
    Add,
    Sub,
    Mul,
    Div,
}

fn apply(op: Op, a: i32, b: i32) -> Option<i32> {
    match op {
        Op::Add => Some(a + b),
        Op::Sub => Some(a - b),
        Op::Mul => Some(a * b),
        Op::Div if b == 0 => None,
        Op::Div => Some(a / b),
    }
}

fn main() {
    println!("{:?}", apply(Op::Div, 6, 0));
}
