`try_claim(&self)`: the first caller gets `true`, the rest `false`. Use `compare_exchange`; do not write `swap` or `store`.
