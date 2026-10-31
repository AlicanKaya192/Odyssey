use std::time::Duration;

async fn add_later(a: i32, b: i32) -> i32 {
    tokio::time::sleep(Duration::from_millis(10)).await;
    a + b
}

#[tokio::main]
async fn main() {
    println!("sum: {}", add_later(40, 2).await);
}
