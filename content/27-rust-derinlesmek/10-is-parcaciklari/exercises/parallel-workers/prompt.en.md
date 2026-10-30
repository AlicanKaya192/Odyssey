Write `fn run_workers(jobs: Vec<i32>) -> Vec<i32>`: a separate branch per job sends twice the job to a channel. Return the results **sorted**. Do not forget `drop(tx)`, or the program hangs.
