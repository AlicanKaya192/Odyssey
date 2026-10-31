macro_rules! make_struct {
    ($name:ident { $( $field:ident : $t:ty ),* $(,)? }) => {
        struct $name {
            $( $field: $t, )*
        }

        impl $name {
            $(
                fn $field(&self) -> &$t {
                    &self.$field
                }
            )*
        }
    };
}

make_struct!(Point { x: i32, y: i32 });

fn main() {
    let point = Point { x: 3, y: 4 };
    println!("{} {}", point.x(), point.y());
}
