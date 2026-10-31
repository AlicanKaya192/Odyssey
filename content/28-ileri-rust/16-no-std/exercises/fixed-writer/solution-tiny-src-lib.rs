#![no_std]

use core::fmt::{self, Write};

pub struct Buffer<'a> {
    bytes: &'a mut [u8],
    len: usize,
}

impl<'a> Buffer<'a> {
    pub fn new(bytes: &'a mut [u8]) -> Self {
        Buffer { bytes, len: 0 }
    }

    pub fn as_bytes(&self) -> &[u8] {
        &self.bytes[..self.len]
    }
}

impl Write for Buffer<'_> {
    fn write_str(&mut self, text: &str) -> fmt::Result {
        let end = self.len + text.len();
        if end > self.bytes.len() {
            return Err(fmt::Error);
        }
        self.bytes[self.len..end].copy_from_slice(text.as_bytes());
        self.len = end;
        Ok(())
    }
}

pub fn report(out: &mut Buffer, name: &str, value: i32) -> fmt::Result {
    write!(out, "{name}={value}")
}
