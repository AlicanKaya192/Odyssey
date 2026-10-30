fn parse_pair(line: &str) -> Result<(String, i32), String> {
    let (key, value) = line.split_once('=').ok_or(format!("no equals: {line}"))?;
    let number = value.trim().parse::<i32>().map_err(|_| format!("bad value: {value}"))?;
    Ok((key.trim().to_string(), number))
}

fn main() {
    println!("{:?}", parse_pair("a = 1"));
}
