Write `fn read_all(value: i32, readers: usize) -> i32`: the value is in an `Arc<RwLock<i32>>`. `readers` branches read, each returns the value, and give the total.
