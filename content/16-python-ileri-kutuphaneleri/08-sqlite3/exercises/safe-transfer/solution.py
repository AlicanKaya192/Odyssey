import sqlite3

ADD = "UPDATE accounts SET balance = balance + ? WHERE name = ?"
SUB = "UPDATE accounts SET balance = balance - ? WHERE name = ?"


def transfer(balances, src, dst, amount):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts "
                 "(name TEXT PRIMARY KEY, balance INTEGER CHECK (balance >= 0))")
    conn.executemany("INSERT INTO accounts VALUES (?, ?)", balances.items())
    conn.commit()
    try:
        with conn:
            conn.execute(ADD, (amount, dst))
            conn.execute(SUB, (amount, src))
    except sqlite3.IntegrityError:
        pass
    return dict(conn.execute("SELECT name, balance FROM accounts"))

print(transfer({"ada": 100, "alan": 20}, "ada", "alan", 30))
print(transfer({"ada": 100, "alan": 20}, "alan", "ada", 500))
