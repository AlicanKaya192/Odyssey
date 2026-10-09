Write the function `two_sum(numbers, target)`: in an **unsorted** list it
returns the **indices** of two elements adding up to `target` as an `(i, j)`
tuple (`i < j`); `None` if there are none.

For each `x`, ask a dictionary (value → index) whether the complement
`target - x` was seen before.

**Speed requirement:** at the end of the code a sum that is not there is
searched for in a list of 200 000 numbers; a nested loop would not make it in
time.

**Expected output:**

```
(3, 4)
(0, 1)
None
```
