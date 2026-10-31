Write `store_max(target, value)`: if `target` is below `value`, make it `value`. Use a `compare_exchange_weak` loop, not `fetch_max`.
