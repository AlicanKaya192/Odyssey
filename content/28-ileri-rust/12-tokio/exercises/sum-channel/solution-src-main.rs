use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    for n in 1..=4 {
        let sender = sender.clone();
        tokio::spawn(async move {
            sender.send(n).await.unwrap();
        });
    }
    drop(sender);

    let mut total: i32 = 0;
    while let Some(n) = receiver.recv().await {
        total += n;
    }
    println!("total: {total}");
}
