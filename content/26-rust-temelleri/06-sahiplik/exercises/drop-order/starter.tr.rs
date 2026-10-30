struct Tracker(&'static str);

impl Drop for Tracker {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    // Tracker("a") gibi değerler oluştur: let _a = Tracker("a");
}
