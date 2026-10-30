fn word_count(text: &str) -> usize {
    text.split_whitespace().count()
}

fn is_short(text: &str) -> bool {
    word_count(text) < 3
}

fn main() {
    println!("{}", is_short("a b"));
}

#[cfg(test)]
mod tests {
    use super::*;

    // #[test] ile en az 3 test yaz
}
