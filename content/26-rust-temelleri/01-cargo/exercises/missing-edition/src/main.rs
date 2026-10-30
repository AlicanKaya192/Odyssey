async fn later() {}

fn main() {
    let _pending = later();
    println!("edition ok");
}
