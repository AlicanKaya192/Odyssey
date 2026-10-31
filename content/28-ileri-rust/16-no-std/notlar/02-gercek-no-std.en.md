## From a library to a program

Throughout the lesson we wrote a `no_std` library. A real `no_std` **program** (running on a device) also needs the following, because nobody does `std`'s jobs any more:

| Missing | Solution |
|---|---|
| What happens on a panic | `#[panic_handler]` |
| Where the program starts | `#![no_main]` and the device's startup code |
| A memory allocator (if `alloc` is used) | `#[global_allocator]` |
| The target | Such as `--target thumbv7em-none-eabihf` |

This program cannot run on a desktop, which is why in Odyssey we only tried libraries.

## The panic handler

In `no_std`, you decide what a panic does:

```rust
#![no_std]

use core::panic::PanicInfo;

#[panic_handler]
fn on_panic(_info: &PanicInfo) -> ! {
    loop {}
}
```

This code compiles (we measured it with `cargo build -p tiny`). The return type is `!`, because nothing continues after a panic. On a device it usually lights an error lamp and waits, or restarts.

Note: a library does not write `panic_handler`. A program can have only one, and `std` already brings one; both together do not compile. The handler is the final program's job.

## The device side

| Concept | Meaning |
|---|---|
| Target | A triple of processor and environment; added with `rustup target add` |
| `none` | In a target name, means no operating system |
| Memory map | Where code and data are placed, with a linker script |
| Peripheral | Hardware controlled by writing to a memory address |
| `volatile` | So the compiler does not remove this read or write |

The tool for the last row is `core::ptr::read_volatile` and `write_volatile`.

## Known names

| Crate | Its job |
|---|---|
| `embassy` | An embedded async executor |
| `heapless` | Fixed-capacity `Vec` and `String` |
| `embedded-hal` | Shared traits for hardware |
| `cortex-m-rt` | ARM startup code |
| `libm` | Floating-point math |

They are not installed in this path; knowing their names is enough.

## When to think about it?

Even if you do not write embedded code, adding `no_std` support to your library makes it usable everywhere and stops it binding to the operating system by accident. Making the split early is cheap; adding it later is expensive. But if you are writing an application, use `std`: this is not a virtue, it is a need.
