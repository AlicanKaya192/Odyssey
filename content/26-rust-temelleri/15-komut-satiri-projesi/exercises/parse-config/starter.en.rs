struct Config {
    pattern: String,
    path: String,
}

// fn parse_args ...

fn main() {
    let args = vec![String::from("search"), String::from("a"), String::from("f.txt")];
    let config = parse_args(&args).expect("valid");
    println!("{} {}", config.pattern, config.path);
}
