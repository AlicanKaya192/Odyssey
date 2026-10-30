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

    // write a test with #[should_panic]
}
