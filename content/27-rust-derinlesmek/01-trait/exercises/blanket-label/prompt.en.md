Write `trait Label { fn label(&self) -> String; }` and implement it with a single `impl` for **every type** providing `Debug`: the result has the form `<{:?}>`. Example: `5.label()` → `<5>`.
