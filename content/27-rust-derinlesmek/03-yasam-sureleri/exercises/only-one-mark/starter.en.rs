// fn pick ...

fn main() {
    let line = String::from("a,b,c");
    let found;
    {
        let label = String::from("last");
        found = pick(&line, &label);
    }
    println!("{found}");
}
