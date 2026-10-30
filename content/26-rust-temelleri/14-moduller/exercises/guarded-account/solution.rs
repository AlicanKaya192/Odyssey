mod bank {
    pub struct Account {
        balance: i64,
    }

    impl Account {
        pub fn new() -> Account {
            Account { balance: 0 }
        }

        pub fn deposit(&mut self, amount: i64) -> Result<(), String> {
            if amount <= 0 {
                return Err(String::from("amount must be positive"));
            }
            self.balance += amount;
            Ok(())
        }

        pub fn balance(&self) -> i64 {
            self.balance
        }
    }
}

fn main() {
    let mut a = bank::Account::new();
    println!("{:?}", a.deposit(5));
    println!("{}", a.balance());
}
