const VAT_PERCENT: u32 = 20;

fn main() {
    let base = 250;
    let tax = base * VAT_PERCENT / 100;
    let total = base + tax;
    println!("base  {:>6}", base);
    println!("tax   {:>6}", tax);
    println!("total {:>6}", total);
}
