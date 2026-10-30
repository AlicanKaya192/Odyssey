`insert(index, value)` and `remove(index)`: shift the rest with `ptr::copy`. Out of bounds, panic with `assert!`.
