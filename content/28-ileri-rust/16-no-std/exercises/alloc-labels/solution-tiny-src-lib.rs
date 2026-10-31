#![no_std]

extern crate alloc;

use alloc::format;
use alloc::string::String;
use alloc::vec::Vec;

pub fn labels(values: &[i32]) -> Vec<String> {
    values.iter().map(|value| format!("#{value}")).collect()
}
