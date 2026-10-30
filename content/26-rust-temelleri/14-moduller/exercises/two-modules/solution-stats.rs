pub fn mean(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    let mut total = 0.0;
    for v in values {
        total += v;
    }
    Some(total / values.len() as f64)
}
