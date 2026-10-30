fn split_pair<'a>(line: &'a str) -> Option<(&'a str, &'a str)> {
    let (left, right) = line.split_once(':')?;
    Some((left.trim(), right.trim()))
}

fn main() {
    println!("{:?}", split_pair("a : b"));
}
