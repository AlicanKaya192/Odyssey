mod rt;

use rt::{ChanReceiver, Spawner, async_channel, executor, run, spawn};
use std::collections::BTreeMap;

// fn word_totals(spawner: &Spawner, lines: Vec<&'static str>) -> rt::JoinHandle<BTreeMap<String, u32>> ...

fn main() {
    let (spawner, queue) = executor();
    let lines = vec!["one two", "two three", "three three"];
    let handle = word_totals(&spawner, lines);
    spawner.detach(async move {
        println!("{:?}", handle.await);
    });
    drop(spawner);
    run(queue);
}
