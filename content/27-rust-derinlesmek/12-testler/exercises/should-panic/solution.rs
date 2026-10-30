fn checked_age(age: i32) -> i32 {
    if age < 0 {
        panic!("age must not be negative");
    }
    age
}

fn main() {
    println!("{}", checked_age(3));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "negative")]
    fn negative_panics() {
        checked_age(-1);
    }

    #[test]
    fn keeps_zero() {
        assert_eq!(checked_age(0), 0);
    }
}
