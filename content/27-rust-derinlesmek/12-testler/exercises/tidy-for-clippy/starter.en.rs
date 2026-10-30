fn total(list: &Vec<i32>) -> i32 {
    let mut sum = 0;
    for i in 0..list.len() {
        sum += list[i];
    }
    return sum;
}

fn is_empty_list(list: &Vec<i32>) -> bool {
    if list.len() == 0 {
        return true;
    } else {
        return false;
    }
}

fn main() {
    let list = vec![1, 2];
    println!("{} {}", total(&list), is_empty_list(&list));
}
