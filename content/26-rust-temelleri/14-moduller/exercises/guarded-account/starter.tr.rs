// mod bank { ... }

fn main() {
    let mut a = bank::Account::new();
    println!("{:?}", a.deposit(5));
    println!("{}", a.balance());
}
