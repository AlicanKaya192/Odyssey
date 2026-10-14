`shipping.py` (in the other tab, read-only) calculates a shipping cost:

- Up to 1 kg: `5`
- Up to 5 kg: `9`
- Above that: `9` + `2` for each extra kg

Write at least **three** tests in `main.py`:

- `shipping_cost(1)` → `5`
- `shipping_cost(5)` → `9`
- `shipping_cost(7)` → `13`

Each test is a function whose name starts with `test_`. Odyssey will run your tests on the correct code and on versions broken on purpose.
