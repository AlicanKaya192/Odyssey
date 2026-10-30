`set`: the first caller writes and gets `true`, the rest `false`. `get`: `Some(&T)` if `READY`. Three states: `EMPTY`, `WRITING`, `READY`. Do not use `OnceLock`.
