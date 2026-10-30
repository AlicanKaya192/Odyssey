fn keep<F: Fn(i32) -> bool>(values: &[i32], test: F) -> Vec<i32> {
    let mut out = Vec::new();
    for v in values {
        if test(*v) {
            out.push(*v);
        }
    }
    out
}

fn each_total(values: &[i32], mut report: impl FnMut(i32)) {
    let mut total = 0;
    for v in values {
        total += v;
        report(total);
    }
}

fn main() {
    let limit = 2;
    println!("{:?}", keep(&[1, 2, 3], |n| n > limit));
    let mut seen = Vec::new();
    each_total(&[1, 2, 3], |t| seen.push(t));
    println!("{:?}", seen);
}
