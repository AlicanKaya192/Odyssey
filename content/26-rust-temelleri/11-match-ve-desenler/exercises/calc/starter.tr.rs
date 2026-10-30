enum Op {
    Add,
    Sub,
    Mul,
    Div,
}

// fn apply ...

fn main() {
    println!("{:?}", apply(Op::Div, 6, 0));
}
