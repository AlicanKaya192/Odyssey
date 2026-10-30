struct Config {
    pattern: String,
    path: String,
}

fn parse_args(args: &[String]) -> Result<Config, String> {
    if args.len() != 3 {
        return Err(String::from("usage: search <pattern> <file>"));
    }
    Ok(Config { pattern: args[1].clone(), path: args[2].clone() })
}

fn main() {
    let args = vec![String::from("search"), String::from("a"), String::from("f.txt")];
    let config = parse_args(&args).expect("valid");
    println!("{} {}", config.pattern, config.path);
}
