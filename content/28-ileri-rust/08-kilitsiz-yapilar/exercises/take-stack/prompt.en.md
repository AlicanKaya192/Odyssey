`push`: put a new node at the head with a `compare_exchange_weak` loop. `take_all`: empty the head with `swap`, and convert the chain to a `Vec` with `Box::from_raw` (last added first).
