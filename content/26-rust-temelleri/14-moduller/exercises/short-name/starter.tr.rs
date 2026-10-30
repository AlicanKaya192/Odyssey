mod tools {
    pub mod text {
        pub fn shout(s: &str) -> String {
            s.to_uppercase()
        }
    }
}

fn main() {
    println!("{}", tools::text::shout("hi"));
}
