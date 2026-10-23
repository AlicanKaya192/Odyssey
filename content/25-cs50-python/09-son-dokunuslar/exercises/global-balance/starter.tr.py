balance = 0


def main():
    deposit(int(input("Deposit: ")))
    withdraw(int(input("Withdraw: ")))
    print("Balance:", balance)


def deposit(n):
    balance += n


def withdraw(n):
    balance -= n


if __name__ == "__main__":
    main()
