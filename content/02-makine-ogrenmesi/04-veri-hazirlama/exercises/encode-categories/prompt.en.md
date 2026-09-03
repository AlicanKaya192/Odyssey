The previous exercise left two columns out: `fuel` and `gearbox`. Being
text, they could not enter the model. Now they will.

**What you need to do:**

1. Read the file. This time take **five** columns: `age`, `km`, `engine`,
   `fuel`, `gearbox`. The target is still `price`.
2. **One-hot** encode `fuel` and `gearbox` — each category gets its own
   column.
3. Print how many columns there are after encoding.
4. Print the column names, **sorted**.
5. Split (`random_state=42`), fill the `engine` gaps with the **training**
   mean, train the model.
6. Print the MAE (two decimals).
7. The previous exercise's MAE was **32.58**. Print `better` if the new
   model beats it, `worse` otherwise.

**Expected output:**

```
8
['age', 'engine', 'fuel_diesel', 'fuel_lpg', 'fuel_petrol', 'gearbox_auto', 'gearbox_manual', 'km']
16.42
better
```

**The error halved:** 32.58 → 16.42. Fuel type and gearbox really do drive
the price; they had been left out only because they were not numbers.

**Why a separate column per category:** saying `petrol=0, diesel=1, lpg=2`
would teach the model that `lpg` is twice `petrol` and `diesel` exactly
halfway between. No such ordering exists. One-hot encoding describes all
three categories without inventing an order.

**When the order really exists, this changes:** `low < medium < high` or
`primary < secondary < university` take `0, 1, 2` correctly — that is called
ordinal encoding.

**A trap:** a column with hundreds of categories (a city, a product code)
produces hundreds of columns under one-hot. On 120 rows that pushes the
number of features towards the number of samples and the model starts
memorising.
