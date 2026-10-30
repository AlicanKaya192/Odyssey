fn main() {
    let mut log = String::from("start");
    let view = &log;
    println!("{view}");
    log.push_str(" end");
    println!("{log}");
}
