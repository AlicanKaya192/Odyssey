Write the `ThreadWaker` struct, its `Wake` implementation and `block_on`. On `Pending`, sleep with `thread::park()`; `wake` wakes the branch with `unpark`. Do not use `Waker::noop()`.
