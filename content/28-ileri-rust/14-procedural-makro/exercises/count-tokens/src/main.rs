use my_macros::count_tokens;

fn main() {
    println!("{}", count_tokens!());
    println!("{}", count_tokens!(a b c));
    println!("{}", count_tokens!(1 + (2 * 3)));
    let doubled = count_tokens!(x y) * 2;
    println!("{doubled}");
}
