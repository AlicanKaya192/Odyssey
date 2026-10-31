fn main() {
    let first = "Grace";
    let last = "Hopper";
    let full = format!("{first} {last}");
    println!("{full}");
    println!("letters: {}", full.chars().count());
}
