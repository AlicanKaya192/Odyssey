fn main() {
    let total = 2.0 * 3.5 + 1.0 * 12.25;
    println!("{:<8}{:>4}{:>8}", "item", "qty", "price");
    println!("{:<8}{:>4}{:>8.2}", "tea", 2, 3.5);
    println!("{:<8}{:>4}{:>8.2}", "coffee", 1, 12.25);
    println!("{:<8}{:>4}{:>8.2}", "total", "", total);
}
