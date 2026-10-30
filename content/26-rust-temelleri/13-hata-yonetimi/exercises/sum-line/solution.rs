fn sum_line(line: &str) -> Result<i32, String> {
    let mut total = 0;
    for token in line.split_whitespace() {
        let n = token.parse::<i32>().map_err(|_| format!("bad number: {token}"))?;
        total += n;
    }
    Ok(total)
}

fn main() {
    println!("{:?}", sum_line("1 2 3"));
    println!("{:?}", sum_line("1 x"));
}
