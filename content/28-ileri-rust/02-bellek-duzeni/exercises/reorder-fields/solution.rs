#[repr(C)]
struct Record {
    id: u32,
    active: u8,
    level: u8,
}

fn make() -> Record {
    Record { active: 1, id: 7, level: 2 }
}

fn main() {
    let r = make();
    println!("{} {} {}", r.active, r.id, r.level);
    println!("{}", size_of::<Record>());
}
