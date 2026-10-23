Bitcoin is a cryptocurrency: rather than relying on a bank, it relies on a distributed network that records transactions (a blockchain).

Implement a program that:

- Expects the number of Bitcoins the user would like to buy, `n`, as a **command-line argument**. With no argument it exits via `sys.exit("Missing command-line argument")`; if the argument cannot be converted to a `float`, via `sys.exit("Command-line argument is not a number")`.
- Asks the API for the Bitcoin price: `http://api.odyssey.test/v3/assets/bitcoin`. The response is a JSON object; the price is under the `priceUsd` key inside `data`, as a string. Catch `requests.RequestException`.
- Outputs the cost of `n` Bitcoins in USD **to four decimal places**, with `,` as the thousands separator: `$97,534.2892`.

In CS50 the request goes to CoinCap's real API and needs an API key. Here Odyssey has its own exercise server: it answers in the same format, does not go out to the internet, and its price is **fixed**. (In CS50 the file is `bitcoin.py`.)

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- No input → output (nothing) (exit code 1)
- Command `python cozum.py cat` → output (nothing) (exit code 1)
- Command `python cozum.py 1` → output `$97,534.2892`
- Command `python cozum.py 2` → output `$195,068.5783`
- Command `python cozum.py 2.5` → output `$243,835.7229`
- Command `python cozum.py 0.001` → output `$97.5343`
