struct Windows2<'a, T> {
    items: &'a [T],
    index: usize,
}

impl<'a, T> Iterator for Windows2<'a, T> {
    type Item = &'a [T];

    fn next(&mut self) -> Option<&'a [T]> {
        if self.index + 2 > self.items.len() {
            return None;
        }
        let part = &self.items[self.index..self.index + 2];
        self.index += 1;
        Some(part)
    }
}

fn main() {
    let list = [1, 2, 3];
    for w in (Windows2 { items: &list, index: 0 }) {
        println!("{:?}", w);
    }
}
