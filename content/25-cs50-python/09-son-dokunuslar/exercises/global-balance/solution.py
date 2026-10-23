balance = 0


def main():
    deposit(int(input("Deposit: ")))
    withdraw(int(input("Withdraw: ")))
    print("Balance:", balance)


def deposit(n):
    global balance
    balance += n


def withdraw(n):
    global balance
    balance -= n


if __name__ == "__main__":
    main()
