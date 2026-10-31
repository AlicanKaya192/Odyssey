use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    let address = listener.local_addr()?;
    drop(listener); // Start the server task instead

    for word in ["rust", "tokio"] {
        let mut client = TcpStream::connect(address).await?;
        client.write_all(word.as_bytes()).await?;
        let mut buffer = [0; 64];
        let n = client.read(&mut buffer).await?;
        println!("{}", String::from_utf8_lossy(&buffer[..n]));
    }
    Ok(())
}
