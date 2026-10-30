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

fn step(state: State, event: Event) -> State {
    match (state, event) {
        (State::Idle, Event::Coin) => State::HasCoin,
        (State::HasCoin, Event::Select) => State::Dispensing,
        (State::Dispensing, Event::Done) => State::Idle,
        (other, _) => other,
    }
}

fn main() {
    println!("{:?}", step(State::Idle, Event::Coin));
}
