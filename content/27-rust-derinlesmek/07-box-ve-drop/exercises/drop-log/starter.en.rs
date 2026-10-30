struct Log<'a> {
    lines: &'a mut Vec<String>,
    name: String,
}

// impl Drop ...

fn run(lines: &mut Vec<String>) {
    let _log = Log { lines, name: String::from("run") };
}

fn main() {
    let mut lines = Vec::new();
    run(&mut lines);
    println!("{:?}", lines);
}
