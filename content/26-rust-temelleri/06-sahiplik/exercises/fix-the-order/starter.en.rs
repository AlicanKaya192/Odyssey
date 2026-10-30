fn announce(text: String) {
    println!("announcing {text}");
}

fn main() {
    let news = String::from("release");
    announce(news);
    println!("{news} is ready");
}
