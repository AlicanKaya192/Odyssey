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

    #[test]
    fn divides() {
        assert_eq!(safe_div(6, 3), Some(2));
    }

    #[test]
    fn zero_gives_none() {
        assert_eq!(safe_div(1, 0), None);
    }

    #[test]
    fn clamps_low_and_high() {
        assert_eq!(clamp_score(-1), 0);
        assert_eq!(clamp_score(101), 100);
    }

    #[test]
    fn keeps_boundaries() {
        assert_eq!(clamp_score(0), 0);
        assert_eq!(clamp_score(100), 100);
        assert_eq!(clamp_score(50), 50);
    }
}
