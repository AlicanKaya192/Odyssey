use std::fmt;
use std::num::ParseIntError;

#[derive(Debug, PartialEq)]
enum ConfigError {
    Missing(String),
    BadPort(ParseIntError),
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            ConfigError::Missing(key) => write!(f, "{key} is missing"),
            ConfigError::BadPort(_) => write!(f, "port is not a number"),
        }
    }
}

impl std::error::Error for ConfigError {}

impl From<ParseIntError> for ConfigError {
    fn from(e: ParseIntError) -> Self {
        ConfigError::BadPort(e)
    }
}

fn read_port(lines: &[&str]) -> Result<u16, ConfigError> {
    let value = lines
        .iter()
        .find_map(|line| line.strip_prefix("port="))
        .ok_or_else(|| ConfigError::Missing(String::from("port")))?;
    Ok(value.parse()?)
}

fn main() {
    println!("{:?}", read_port(&["host=a", "port=80"]));
}
