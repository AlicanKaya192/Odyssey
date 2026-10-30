#[cfg(feature = "metric")]
fn label(n: u32) -> String {
    format!("{n} km")
}

#[cfg(not(feature = "metric"))]
fn label(n: u32) -> String {
    format!("{n} miles")
}

fn main() {
    println!("{}", label(10));
}
