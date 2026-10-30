use std::fmt;
use std::num::ParseIntError;

#[derive(Debug, PartialEq)]
enum ConfigError {
    Missing(String),
    BadPort(ParseIntError),
}

// impl fmt::Display for ConfigError ...
// impl std::error::Error for ConfigError {}
// impl From<ParseIntError> for ConfigError ...

// fn read_port(lines: &[&str]) -> Result<u16, ConfigError> ...

fn main() {
    println!("{:?}", read_port(&["host=a", "port=80"]));
}
