use tiny::parse_number;

fn main() {
    println!("{:?}", parse_number("120"));
    println!("{:?}", parse_number(""));
    println!("{:?}", parse_number("12a"));
    println!("{:?}", parse_number("99999999999"));
}
