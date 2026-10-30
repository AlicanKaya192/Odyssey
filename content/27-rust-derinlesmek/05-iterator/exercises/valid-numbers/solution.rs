fn sum_valid(items: &[&str]) -> i32 {
    items.iter().filter_map(|s| s.parse::<i32>().ok()).sum()
}

fn all_or_error(items: &[&str]) -> Result<Vec<i32>, std::num::ParseIntError> {
    items.iter().map(|s| s.parse::<i32>()).collect()
}

fn main() {
    println!("{}", sum_valid(&["1", "x", "3"]));
    println!("{:?}", all_or_error(&["1", "2"]));
}
