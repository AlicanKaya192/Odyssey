struct Account {
    owner: String,
    balance: i64,
}

impl Account {
    fn new(owner: &str) -> Self {
        Self { owner: owner.to_string(), balance: 0 }
    }

    fn deposit(&mut self, amount: i64) {
        self.balance += amount;
    }

    fn withdraw(&mut self, amount: i64) -> bool {
        if amount > self.balance {
            return false;
        }
        self.balance -= amount;
        true
    }

    fn summary(&self) -> String {
        format!("{}: {}", self.owner, self.balance)
    }
}

fn main() {
    let mut a = Account::new("Ada");
    a.deposit(200);
    println!("{}", a.withdraw(50));
    println!("{}", a.summary());
}
