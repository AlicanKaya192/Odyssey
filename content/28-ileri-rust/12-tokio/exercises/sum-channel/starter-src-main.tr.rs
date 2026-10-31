use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    // Dört görev aç, sonra topla
    let total: i32 = 0;
    println!("total: {total}");
}
