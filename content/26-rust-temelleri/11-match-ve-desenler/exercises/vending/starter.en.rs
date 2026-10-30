#[derive(Debug, PartialEq, Clone, Copy)]
enum State {
    Idle,
    HasCoin,
    Dispensing,
}

enum Event {
    Coin,
    Select,
    Done,
}

// fn step ...

fn main() {
    println!("{:?}", step(State::Idle, Event::Coin));
}
