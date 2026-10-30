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

// fn parse_all(lines: &[&str]) -> Result<Vec<i32>, LineError> ...

fn main() {
    println!("{:?}", parse_all(&["1", "2"]));
}
