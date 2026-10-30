struct Local {
    value: i32,
}

fn make_local(value: i32) -> Local {
    Local { value }
}

fn main() {
    println!("{}", make_local(3).value);
}
