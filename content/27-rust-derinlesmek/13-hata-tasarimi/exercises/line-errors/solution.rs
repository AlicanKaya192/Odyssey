use std::fmt;

#[derive(Debug, PartialEq)]
struct LineError {
    line: usize,
    text: String,
}

impl fmt::Display for LineError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "line {}: bad number {}", self.line, self.text)
    }
}

fn parse_all(lines: &[&str]) -> Result<Vec<i32>, LineError> {
    lines
        .iter()
        .enumerate()
        .map(|(i, s)| {
            s.parse::<i32>().map_err(|_| LineError {
                line: i + 1,
                text: s.to_string(),
            })
        })
        .collect()
}

fn main() {
    println!("{:?}", parse_all(&["1", "2"]));
}
