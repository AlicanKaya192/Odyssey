Write `fn count_even(list: &[u32]) -> u32`: split the list into pieces of two (`chunks(2)`), process each on its own branch in a `thread::scope`, and count evens with `AtomicU32`. No lock.
