Write the function `notes(argv)`: build a parser with two subcommands
(`add_subparsers(dest="command", required=True)`): `add` takes a `text`;
`list` takes a `--limit` of type `int` (default 10). Return the text
`"added: <text>"` for `add` and `"listing <limit>"` for `list`.

**Expected output:**

```
added: buy milk
listing 3
listing 10
```
