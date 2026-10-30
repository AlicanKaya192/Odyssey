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

    #[test]
    fn counts_words() {
        assert_eq!(word_count("a b  c"), 3);
        assert_eq!(word_count(""), 0);
    }

    #[test]
    fn two_words_are_short() {
        assert!(is_short("a b"));
    }

    #[test]
    fn three_words_are_not_short() {
        assert!(!is_short("a b c"));
    }
}
