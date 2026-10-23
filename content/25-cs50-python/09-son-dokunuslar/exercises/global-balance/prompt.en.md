The starter code is the lesson's bank program: `balance` is at the top of the file, and `deposit` and `withdraw` change it. But running it gives an `UnboundLocalError`. Fix it by telling the functions that `balance` is a global variable; the program asks for the amount to deposit and to withdraw and prints the final balance.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Deposit: 100
Withdraw: 30
Balance: 70
```
