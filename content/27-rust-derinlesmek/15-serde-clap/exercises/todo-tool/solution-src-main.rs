use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use std::error::Error;
use std::fs;

const FILE: &str = "todo.json";

#[derive(Parser)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    Count,
    Add { text: String },
    List,
}

#[derive(Serialize, Deserialize)]
struct Task {
    id: u32,
    text: String,
}

fn load() -> Result<Vec<Task>, Box<dyn Error>> {
    match fs::read_to_string(FILE) {
        Ok(text) => Ok(serde_json::from_str(&text)?),
        Err(_) => Ok(Vec::new()),
    }
}

fn save(tasks: &[Task]) -> Result<(), Box<dyn Error>> {
    fs::write(FILE, serde_json::to_string(tasks)?)?;
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let cli = Cli::parse();
    let mut tasks = load()?;
    match cli.command {
        Command::Count => println!("{}", tasks.len()),
        Command::Add { text } => {
            let id = tasks.iter().map(|t| t.id).max().unwrap_or(0) + 1;
            tasks.push(Task { id, text });
            save(&tasks)?;
            println!("added {id}");
        }
        Command::List => {
            for task in &tasks {
                println!("{} {}", task.id, task.text);
            }
        }
    }
    Ok(())
}
