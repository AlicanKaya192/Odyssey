**Five fields**

```text
┌ minute (0-59)
│ ┌ hour (0-23, UTC)
│ │ ┌ day of the month (1-31)
│ │ │ ┌ month (1-12)
│ │ │ │ ┌ day of the week (0-6, 0 = Sunday)
│ │ │ │ │
30 2 * * 1
```

**Signs**

| Sign | Meaning | Example |
|---|---|---|
| `*` | Every value | `* * * * *` every minute (on GitHub at most every 5 minutes) |
| `,` | A list | `0 9 * * 1,3,5` Mon, Wed, Fri 09:00 |
| `-` | A range | `0 9 * * 1-5` weekdays 09:00 |
| `/` | A step | `*/15 * * * *` every 15 minutes |

**Examples** (Turkey = UTC + 3)

| cron | UTC | Turkey |
|---|---|---|
| `0 3 * * *` | Every day 03:00 | 06:00 |
| `17 3 * * *` | Every day 03:17 | 06:17 |
| `30 2 * * 1` | Monday 02:30 | Monday 05:30 |
| `0 21 * * 0` | Sunday 21:00 | Sunday 24:00 = Monday 00:00 |
| `0 6 1 * *` | The 1st of every month 06:00 | 09:00 |

**From Turkey time to cron**

1. Subtract 3 from the Turkey time you want.
2. If the result is below 0, add 24 and **move the day back by one**
   (Monday 01:00 Turkey = Sunday 22:00 UTC → `0 22 * * 0`).

**Watch out**

- Day of the week 0 = Sunday. In Python's `weekday()`, 0 = Monday.
- The top of the hour is the busiest moment; pick a minute like `17`
  instead of `0`.
- Write the cron in quotes: `- cron: "17 3 * * *"`. A value starting with
  `*` means something else in unquoted YAML.
