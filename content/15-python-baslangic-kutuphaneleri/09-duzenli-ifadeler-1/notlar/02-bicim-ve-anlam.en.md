## Building a pattern step by step

Do not try to write a long pattern in one go; start from a small piece and
test with sample texts at every step:

1. Write 3–4 samples that must be accepted and 3–4 that must be **rejected**.
2. Write the smallest piece (`\d{2}`) and test it.
3. Add a piece (`\d{2}:`) and test again.
4. Go on until every sample comes out as expected.

The wrong samples matter more than the right ones: a pattern that accepts
text you did not think of while writing it is only caught that way.

## A regex checks the form, not the meaning

For a clock time, `[0-2]\d:[0-5]\d` looks reasonable: the hour starts with
0–2, the minutes with 0–5.

```python
import re

samples = ["09:30", "23:59", "24:00", "29:99", "9:30"]
print([bool(re.fullmatch(r"[0-2]\d:[0-5]\d", s)) for s in samples])


def valid_time(text):
    if not re.fullmatch(r"\d{2}:\d{2}", text):
        return False
    hour, minute = int(text[:2]), int(text[3:])
    return hour < 24 and minute < 60


print([valid_time(s) for s in samples])
```

```text
[True, True, True, False, False]
[True, True, False, False, False]
```

The pattern accepted `24:00`: the form is right but there is no such time.
The pattern could be written even more intricately, but it gets harder to
read. The cleaner way is to split the work: the **regex** checks the **form**
("two digits, a colon, two digits"), **Python** checks the **meaning** (hour
below 24, minute below 60).

The same holds for dates: `\d{4}-\d{2}-\d{2}` accepts `2026-02-30`. After
checking the form with a regex, try really turning it into a date with
`date.fromisoformat`; if it is invalid, it raises `ValueError`.

## Things like e-mail addresses

The rules of e-mail addresses are so broad that a "correct" regex runs to
hundreds of characters. In practice, a simple form check is done
(`\S+@\S+\.\S+`: no spaces, one `@`, a dot after it) and a confirmation mail
is sent to the address. A regex weeds out what is "certainly wrong"; it
cannot answer "does it really exist".

## Where a regex is not needed

| Job | A simpler way |
|---|---|
| Does the text start with `"Error"`? | `text.startswith("Error")` |
| Does it contain `"@"`? | `"@" in text` |
| Split by commas | `text.split(",")` |
| Only digits? | `text.isdigit()` |

If a string method is enough, use it; everyone reading it understands.
A regex is valuable when the pattern is really complex.
