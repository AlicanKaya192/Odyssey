fn pick<'a>(text: &'a str, label: &str) -> &'a str {
    if label == "first" {
        text.split(',').next().unwrap_or("")
    } else {
        text.rsplit(',').next().unwrap_or("")
    }
}

fn main() {
    let line = String::from("a,b,c");
    let found;
    {
        let label = String::from("last");
        found = pick(&line, &label);
    }
    println!("{found}");
}
