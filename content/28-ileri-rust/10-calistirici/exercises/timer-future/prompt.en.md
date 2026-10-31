`Timer::new(ms)`: build the shared state, open a branch, sleep `ms`, set `done`, and wake the waker if any. `poll`: `Ready` if `done`, otherwise store the latest waker and return `Pending`.
