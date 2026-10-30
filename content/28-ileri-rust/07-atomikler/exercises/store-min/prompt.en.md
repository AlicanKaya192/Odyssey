`store_min(slot, value)`: write if `value` is smaller. With a `compare_exchange` loop. Do not use `fetch_min` or `fetch_update`.
