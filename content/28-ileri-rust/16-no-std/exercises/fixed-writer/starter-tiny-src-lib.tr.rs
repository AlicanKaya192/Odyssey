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

// impl Write for Buffer<'_> ...
// pub fn report(out: &mut Buffer, name: &str, value: i32) -> fmt::Result ...
