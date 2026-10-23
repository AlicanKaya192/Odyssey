The starter code has the lesson's `total(galleons, sickles, knuts)`. Below it, write three functions; all three call `total` by **unpacking**, not with indexes (`coins[0]`):

- `total_from_list(coins)`: `coins` is a list in the order `[galleons, sickles, knuts]`
- `total_from_dict(coins)`: `coins` is a dictionary with the keys `galleons`, `sickles`, `knuts` (in any order)
- `total_all(*vaults)`: takes any number of lists and returns the total of all of them; 0 if there are none

Odyssey calls your functions with different inputs and checks what they return.
