#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
enum Size {
    Small,
    Medium,
    Large,
}

fn largest(sizes: &[Size]) -> Option<Size> {
    sizes.iter().max().copied()
}

fn main() {
    println!("{:?}", largest(&[Size::Small, Size::Large]));
}
