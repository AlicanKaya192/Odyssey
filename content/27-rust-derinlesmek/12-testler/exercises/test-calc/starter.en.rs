fn safe_div(a: i32, b: i32) -> Option<i32> {
    if b == 0 {
        None
    } else {
        Some(a / b)
    }
}

fn clamp_score(value: i32) -> i32 {
    if value < 0 {
        0
    } else if value > 100 {
        100
    } else {
        value
    }
}

fn main() {
    println!("{:?} {}", safe_div(6, 3), clamp_score(120));
}

#[cfg(test)]
mod tests {
    use super::*;

    // write at least 4 tests
}
