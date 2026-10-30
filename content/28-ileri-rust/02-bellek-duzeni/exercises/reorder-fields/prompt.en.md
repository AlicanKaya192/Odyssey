`Record` is `repr(C)` and 12 bytes. Only by changing the order of fields, get it to 8 bytes. `repr(C)` stays; do not write `packed`.
