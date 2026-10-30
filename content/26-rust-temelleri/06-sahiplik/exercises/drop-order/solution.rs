struct Tracker(&'static str);

impl Drop for Tracker {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let _a = Tracker("a");
    {
        let _b = Tracker("b");
        println!("inner end");
    }
    let _c = Tracker("c");
    println!("outer end");
}
