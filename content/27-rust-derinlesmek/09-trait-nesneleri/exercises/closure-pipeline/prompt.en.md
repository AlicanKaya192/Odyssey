`fn run(steps: &[Box<dyn Fn(i32) -> i32>], start: i32) -> i32` applies the steps in order. `fn add(n: i32) -> Box<dyn Fn(i32) -> i32>` returns a step adding `n`.
