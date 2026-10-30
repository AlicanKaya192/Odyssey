mod tools {
    pub mod text {
        pub fn shout(s: &str) -> String {
            s.to_uppercase()
        }
    }
}

use tools::text;

fn main() {
    println!("{}", text::shout("hi"));
}
