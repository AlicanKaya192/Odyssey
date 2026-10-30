Write `struct Highlight<'a> { text: &'a str, start: usize, end: usize }`. `part(&self) -> &'a str` returns the slice between, and `len(&self) -> usize` the length.
