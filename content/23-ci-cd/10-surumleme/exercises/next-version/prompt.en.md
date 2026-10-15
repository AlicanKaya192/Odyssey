Write the function `next_version(version, messages)`. It should take the last version's number and the commit messages since then, and return the next version number.

The **prefix** of each message is the part before the first `:` (the whole message if there is no `:`).

- If the prefix ends with `!` or the message contains `BREAKING CHANGE`: MAJOR (`major`)
- Otherwise, if the prefix starts with `feat`: MINOR (`minor`)
- Otherwise, if the prefix starts with `fix`: PATCH (`patch`)
- The others do not change the version.

The **largest** of the messages wins. If none of them changes the version, the number is returned as it is. Use the ready-made `bump` function to raise the number.

**Expected output:**

```
1.4.3
1.5.0
2.0.0
1.4.2
1.0.0
```
