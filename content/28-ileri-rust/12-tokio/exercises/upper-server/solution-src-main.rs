use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    let address = listener.local_addr()?;
    tokio::spawn(async move {
        loop {
            let (mut socket, _) = listener.accept().await.unwrap();
            tokio::spawn(async move {
                let mut buffer = [0; 64];
                let n = socket.read(&mut buffer).await.unwrap();
                let upper = String::from_utf8_lossy(&buffer[..n]).to_uppercase();
                socket.write_all(upper.as_bytes()).await.unwrap();
            });
        }
    });

    for word in ["rust", "tokio"] {
        let mut client = TcpStream::connect(address).await?;
        client.write_all(word.as_bytes()).await?;
        let mut buffer = [0; 64];
        let n = client.read(&mut buffer).await?;
        println!("{}", String::from_utf8_lossy(&buffer[..n]));
    }
    Ok(())
}
