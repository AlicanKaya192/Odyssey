fn main() {
    let year = 2024;
    println!("{year}: {}", year % 4 == 0 && year % 100 != 0 || year % 400 == 0);
    let year = 2023;
    println!("{year}: {}", year % 4 == 0 && year % 100 != 0 || year % 400 == 0);
    let year = 1900;
    println!("{year}: {}", year % 4 == 0 && year % 100 != 0 || year % 400 == 0);
    let year = 2000;
    println!("{year}: {}", year % 4 == 0 && year % 100 != 0 || year % 400 == 0);
}
