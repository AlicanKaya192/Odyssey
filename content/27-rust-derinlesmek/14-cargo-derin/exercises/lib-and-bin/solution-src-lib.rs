pub fn total(prices: &[u32]) -> u32 {
    prices.iter().sum()
}

pub fn describe(prices: &[u32]) -> String {
    format!("{} items, total {}", prices.len(), total(prices))
}
