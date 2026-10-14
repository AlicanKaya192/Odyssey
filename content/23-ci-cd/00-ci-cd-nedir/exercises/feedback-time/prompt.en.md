This time each stage has a duration too: `(name, minutes, passed)`.

Write the function `feedback_minutes(stages)`: after how many minutes does the pipeline's result arrive?

- Add up the stage durations in order.
- If a stage fails, return the total **including that stage** at once: the pipeline stops there and the result arrives.
- If none fails, return the sum of all the durations.

The lines below try the same stages in two different orders. Look at the difference that putting the fast stage first makes.

**Expected output:**

```
slow first: 14
fast first: 1
all pass: 9
```
