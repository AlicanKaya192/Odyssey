use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    host: String,
    port: u16,
    #[serde(default)]
    retries: u32,
    proxy: Option<String>,
}

fn main() {
    let text = r#"{"host": "localhost", "port": 8080}"#;
    let config: Config = serde_json::from_str(text).unwrap();
    println!("{}:{}", config.host, config.port);
    println!("retries: {}", config.retries);
    println!("proxy: {:?}", config.proxy);
}
