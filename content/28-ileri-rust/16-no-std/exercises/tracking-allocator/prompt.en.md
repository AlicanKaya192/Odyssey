Write `GlobalAlloc` for `Tracking`. `alloc` adds `layout.size()` to `BYTES`, `dealloc` subtracts it, and `System` does the real work.
