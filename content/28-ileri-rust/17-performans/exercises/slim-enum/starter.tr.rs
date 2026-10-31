enum Message {
    Ping,
    Text(String),
    Blob([u8; 256]),
}

impl Message {
    fn text(value: &str) -> Self {
        Message::Text(value.to_string())
    }

    fn blob() -> Self {
        Message::Blob([0; 256])
    }

    fn payload(&self) -> usize {
        match self {
            Message::Ping => 0,
            Message::Text(text) => text.len(),
            Message::Blob(bytes) => bytes.len(),
        }
    }
}

fn main() {
    let messages = [Message::Ping, Message::text("hi"), Message::blob()];
    let sizes: Vec<usize> = messages.iter().map(Message::payload).collect();
    println!("{sizes:?}");
    println!("{}", size_of::<Message>() <= 24);
}
