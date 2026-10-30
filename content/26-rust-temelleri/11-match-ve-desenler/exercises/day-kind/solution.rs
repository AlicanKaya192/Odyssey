fn day_kind(day: u8) -> &'static str {
    match day {
        1..=5 => "weekday",
        6 | 7 => "weekend",
        _ => "invalid",
    }
}

fn main() {
    println!("{}", day_kind(6));
}
