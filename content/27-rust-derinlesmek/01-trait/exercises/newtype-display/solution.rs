use std::fmt::{self, Display};

struct Scores(Vec<u32>);

impl Display for Scores {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut total = 0;
        for s in &self.0 {
            total += s;
        }
        write!(f, "{} scores, total {}", self.0.len(), total)
    }
}

fn main() {
    println!("{}", Scores(vec![1, 2, 3]));
}
