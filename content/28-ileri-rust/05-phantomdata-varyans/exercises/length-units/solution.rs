use std::marker::PhantomData;
use std::ops::Add;

struct Meters;
struct Feet;

struct Length<U> {
    value: i64,
    _unit: PhantomData<U>,
}

fn length<U>(value: i64) -> Length<U> {
    Length { value, _unit: PhantomData }
}

impl<U> Add for Length<U> {
    type Output = Length<U>;

    fn add(self, other: Length<U>) -> Length<U> {
        length(self.value + other.value)
    }
}

impl Length<Meters> {
    fn to_feet_rounded(&self) -> Length<Feet> {
        length(self.value * 3)
    }
}

fn main() {
    let a: Length<Meters> = length(2) + length(3);
    println!("{}", a.value);
}
