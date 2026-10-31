use std::time::Duration;
use tokio::time::{sleep, timeout};

async fn fetch(wait_ms: u64) -> i32 {
    sleep(Duration::from_millis(wait_ms)).await;
    7
}

async fn fetch_or_default(wait_ms: u64) -> i32 {
    match timeout(Duration::from_millis(50), fetch(wait_ms)).await {
        Ok(value) => value,
        Err(_) => -1,
    }
}

#[tokio::main]
async fn main() {
    println!("{}", fetch_or_default(1).await);
    println!("{}", fetch_or_default(2000).await);
}
