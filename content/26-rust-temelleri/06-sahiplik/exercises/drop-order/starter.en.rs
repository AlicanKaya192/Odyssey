struct Tracker(&'static str);

impl Drop for Tracker {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    // Create values such as Tracker("a"): let _a = Tracker("a");
}
