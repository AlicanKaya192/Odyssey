For this exercise there is a second file called `toolbox.py` sitting **next
to** yours. This is what is in it:

```python
# toolbox.py

TAX_RATE = 0.20


def with_tax(price):
    return price + price * TAX_RATE


def discount(price, percent):
    return price - price * percent / 100
```

You did not write this file, but it is a module all the same — there is no
difference between it and `math`. To use what is inside you have to bring it
in first.

Note that the module does not hold only functions: there is also a **value**
called `TAX_RATE`. You can reach it the same way.

**What to do:**

1. Bring in the `toolbox` module.
2. The `price` variable is `250`. Create three variables:

| Variable | What goes in it |
|---|---|
| `final_price` | The price with tax added |
| `sale_price` | The price with a ten percent discount |
| `rate` | The tax rate from the module |

3. Print the three of them **on separate lines**.

**Expected output:**

```
300.0
225.0
0.2
```
