fn main() {
    let steps = [4200, 8100, 6000, 7300, 5150];
    let total = steps[0] + steps[1] + steps[2] + steps[3] + steps[4];
    let count = steps.len();
    let average = total as f64 / count as f64;
    println!("days: {count}");
    println!("total: {total}");
    println!("average: {average:.2}");
}
