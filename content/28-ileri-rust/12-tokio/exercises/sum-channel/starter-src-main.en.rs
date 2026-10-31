use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    // Start four tasks, then add up
    let total: i32 = 0;
    println!("total: {total}");
}
