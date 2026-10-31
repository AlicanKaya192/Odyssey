use std::time::{Duration, Instant};

async fn job(n: u32) -> u32 {
    tokio::time::sleep(Duration::from_millis(200)).await;
    n * 2
}

#[tokio::main]
async fn main() {
    let start = Instant::now();
    let a = job(1).await;
    let b = job(2).await;
    let c = job(3).await;
    println!("{a} {b} {c}");
    println!("fast: {}", start.elapsed().as_millis() < 500);
}
