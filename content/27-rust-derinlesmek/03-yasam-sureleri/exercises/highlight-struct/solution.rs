struct Highlight<'a> {
    text: &'a str,
    start: usize,
    end: usize,
}

impl<'a> Highlight<'a> {
    fn part(&self) -> &'a str {
        &self.text[self.start..self.end]
    }

    fn len(&self) -> usize {
        self.end - self.start
    }
}

fn main() {
    let h = Highlight { text: "hello world", start: 6, end: 11 };
    println!("{} {}", h.part(), h.len());
}
