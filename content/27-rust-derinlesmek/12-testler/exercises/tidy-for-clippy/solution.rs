fn total(list: &[i32]) -> i32 {
    list.iter().sum()
}

fn is_empty_list(list: &[i32]) -> bool {
    list.is_empty()
}

fn main() {
    let list = vec![1, 2];
    println!("{} {}", total(&list), is_empty_list(&list));
}
