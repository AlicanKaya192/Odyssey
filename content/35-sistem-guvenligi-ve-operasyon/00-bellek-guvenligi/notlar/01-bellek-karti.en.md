## The family of bugs

| Bug | In short | Prevention |
|---|---|---|
| Buffer overflow | Writing past the end of the region | Check the size before writing |
| Out-of-bounds read | Reading outside the region | Check the length to read |
| Off-by-one | Counting the bound one too many | `range(size)`, a bound with `<` |
| Integer overflow | The size calculation wraps | Check it fits before calculating |
| Use-after-free | Using memory that was given back | Clear the pointer, a safe language |
| Double free | Giving the same memory back twice | Keep ownership in one place |

## Dangerous and safe counterparts in C

| Dangerous | Why? | Instead |
|---|---|---|
| `gets` | Never limits the line length | `fgets` |
| `strcpy` | Does not know the target's size | `strncpy`, `strlcpy` |
| `strcat` | Does not know the append will fit | `strncat`, `strlcat` |
| `sprintf` | Does not know the output's size | `snprintf` |

Watch out when searching: `fgets` contains `gets` and `snprintf` contains
`printf`. Use a word boundary when searching for a name (`\bgets\s*\(`),
otherwise the safe counterpart is caught too.

## Python patterns

- Bounds check: `if len(data) > size: ...` **before** writing.
- Truncating: `data[:size]`.
- Imitating an 8-bit wrap: `n & 0xFF`; for 16 bits `n & 0xFFFF`.
- Does it fit: `a + b < 2 ** bits`.

## Keep in mind

- An overflow is **silent**: the program does not stop, it carries on with
  the wrong data.
- In C the zero byte at the end of a string takes space too: 9 bytes for 8
  letters.
- Every length that comes from outside (a packet, a file, a form) is
  untrusted; it is measured first, then used.
