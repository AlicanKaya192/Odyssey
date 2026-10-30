use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("usage: wc <file>");
        process::exit(2);
    }
    let text = match fs::read_to_string(&args[1]) {
        Ok(text) => text,
        Err(_) => {
            eprintln!("cannot read {}", args[1]);
            process::exit(2);
        }
    };
    println!("{} {}", text.lines().count(), text.split_whitespace().count());
}
