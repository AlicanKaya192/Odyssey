fn letter(score: i32) -> char {
    if score >= 90 {
        'A'
    } else if score >= 70 {
        'B'
    } else if score >= 50 {
        'C'
    } else {
        'F'
    }
}

fn main() {
    println!("{}", letter(72));
}
