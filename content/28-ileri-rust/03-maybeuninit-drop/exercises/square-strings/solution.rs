use std::mem::MaybeUninit;

fn squares() -> [String; 4] {
    let mut slots: [MaybeUninit<String>; 4] = [const { MaybeUninit::uninit() }; 4];
    for (i, slot) in slots.iter_mut().enumerate() {
        slot.write((i * i).to_string());
    }
    // SAFETY: the loop wrote all four slots.
    unsafe { slots.map(|slot| slot.assume_init()) }
}

fn main() {
    println!("{:?}", squares());
}
