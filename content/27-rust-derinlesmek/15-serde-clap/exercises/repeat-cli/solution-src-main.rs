use clap::Parser;

#[derive(Parser)]
struct Cli {
    word: String,
    #[arg(short, long, default_value_t = 1)]
    times: u32,
    #[arg(short, long)]
    upper: bool,
}

fn main() {
    let cli = Cli::parse();
    let word = if cli.upper { cli.word.to_uppercase() } else { cli.word };
    for _ in 0..cli.times {
        println!("{word}");
    }
}
