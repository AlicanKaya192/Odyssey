// struct Account ...

fn main() {
    let mut a = Account::new("Ada");
    a.deposit(200);
    println!("{}", a.withdraw(50));
    println!("{}", a.summary());
}
