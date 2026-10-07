Save the `team` list to a JSON file and read it back.

**What to do:**

1. Write `team` to the file `team.json` with `json.dump`, giving
   `indent=2` (`"w"` mode, `encoding="utf-8"`).
2. Open the file again and read it into a variable called `loaded` with
   `json.load`.
3. Print, in order: `loaded == team`, the number of people in the team and
   the number of people whose role is `"dev"` (`dev_count`).

**Expected output:**

```text
True
3
2
```

If the first line is `True`, the list you wrote went to the file and came
back **exactly the same**.
