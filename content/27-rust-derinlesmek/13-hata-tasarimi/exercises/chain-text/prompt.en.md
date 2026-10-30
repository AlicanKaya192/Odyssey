Write `Error` for `FieldError`, with `source` returning the cause. Then `chain_text(err)`: join the error and all causes with ` -> ` and return it.

Example: `bad field age -> invalid digit found in string`
