use std::marker::PhantomData;

struct Local {
    value: i32,
    _not_send: PhantomData<*const ()>,
}

fn make_local(value: i32) -> Local {
    Local { value, _not_send: PhantomData }
}

fn main() {
    println!("{}", make_local(3).value);
}
