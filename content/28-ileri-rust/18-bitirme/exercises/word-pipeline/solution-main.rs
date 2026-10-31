mod rt;

use rt::{ChanReceiver, Spawner, async_channel, executor, run, spawn};
use std::collections::BTreeMap;

async fn count_words(mut receiver: ChanReceiver<String>) -> BTreeMap<String, u32> {
    let mut totals = BTreeMap::new();
    while let Some(word) = receiver.recv().await {
        *totals.entry(word).or_insert(0) += 1;
    }
    totals
}

fn word_totals(spawner: &Spawner, lines: Vec<&'static str>) -> rt::JoinHandle<BTreeMap<String, u32>> {
    let (sender, receiver) = async_channel();
    for line in lines {
        let sender = sender.clone();
        spawner.detach(async move {
            for word in line.split(' ') {
                sender.send(word.to_string());
            }
        });
    }
    spawn(spawner, count_words(receiver))
}

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
