Add two categories to the `categories` table.

| `code` | `name` |
|---|---|
| `NET` | `Networking` |
| `PRN` | `Printing` |

**With a single `INSERT`.** Two separate commands will not pass the
check.

The reason is not a rule but a measurable difference: with one command
the server says "**2** rows affected", while with two separate commands
the last one says "**1**". The check looks at that number.

So why one command? Because either both rows go in or neither does. If
something goes wrong on the second row, the first one never happened
either — you are not left with half the data.
