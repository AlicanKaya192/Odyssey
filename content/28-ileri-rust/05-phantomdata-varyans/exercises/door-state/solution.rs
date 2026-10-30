use std::marker::PhantomData;

struct Open;
struct Closed;

struct Door<State> {
    name: String,
    _state: PhantomData<State>,
}

fn new_door(name: &str) -> Door<Closed> {
    Door { name: name.to_string(), _state: PhantomData }
}

impl Door<Closed> {
    fn open(self) -> Door<Open> {
        Door { name: self.name, _state: PhantomData }
    }
}

impl Door<Open> {
    fn close(self) -> Door<Closed> {
        Door { name: self.name, _state: PhantomData }
    }

    fn enter(&self) -> String {
        format!("through {}", self.name)
    }
}

fn main() {
    let door = new_door("front").open();
    println!("{}", door.enter());
}
