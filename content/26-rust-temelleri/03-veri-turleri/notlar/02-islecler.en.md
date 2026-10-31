## Common number methods

| Method | Example | Result |
|---|---|---|
| `abs` | `(-5_i32).abs()` | 5 |
| `pow` | `2_i32.pow(10)` | 1024 |
| `min` / `max` | `3.min(9)` | 3 |
| `sqrt` | `9.0_f64.sqrt()` | 3.0 |
| `round` | `2.5_f64.round()` | 3.0 |
| `floor` / `ceil` | `2.5_f64.floor()` | 2.0 |

When calling a method you may need to state the number's type: `9.0.sqrt()` does not compile because the compiler cannot tell whether it is `f32` or `f64`. So you write `9.0_f64`.

Arithmetic, comparison and logic operators are in the next section.
