fn main() {
    let mut log = String::from("start");
    let view = &log;
    log.push_str(" end");
    println!("{view}");
    println!("{log}");
}
