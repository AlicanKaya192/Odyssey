fn announce(text: String) {
    println!("announcing {text}");
}

fn main() {
    let news = String::from("release");
    println!("{news} is ready");
    announce(news);
}
