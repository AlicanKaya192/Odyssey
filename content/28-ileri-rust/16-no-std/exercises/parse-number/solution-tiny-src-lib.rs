#![no_std]

pub fn parse_number(text: &str) -> Option<u32> {
    if text.is_empty() {
        return None;
    }
    let mut total: u32 = 0;
    for letter in text.chars() {
        let digit = letter.to_digit(10)?;
        total = total.checked_mul(10)?.checked_add(digit)?;
    }
    Some(total)
}
