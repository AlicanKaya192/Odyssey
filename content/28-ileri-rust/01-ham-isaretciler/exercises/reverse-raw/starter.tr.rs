// fn reverse_raw(list: &mut [i32]) ...

fn main() {
    let mut list = [1, 2, 3];
    reverse_raw(&mut list);
    println!("{list:?}");
}
