The model extracted the callback time from the customer's message as JSON:
`{"date": "YYYY-MM-DD", "time": "HH:MM", "source": "..."}` (`source` is the
customer's own words). `check_callback(message, reply, now)` should check
the model's answer (`reply`, a text) against the reference time `now` (ISO
text) and return one of these, applying the rules in this order:

1. `"rejected"` if the JSON cannot be read, is not a dictionary or its
   fields are not exactly these three.
2. `"rejected"` if `source` in lower case does not fully match the form
   `today at 9am` / `tomorrow at 7pm` (`re.fullmatch`, `am`/`pm` optional)
   or does not appear in the message (ignoring case).
3. `"needs_clarification"` if there is no `am`/`pm`.
4. `"rejected"` if the hour is not 1–12.
5. `"rejected"` if `date` and `time` differ from the ones calculated from
   the reference (`12am` = `00:00`), otherwise `"accepted"`.

**Expected output:**

```
accepted
needs_clarification
rejected
```
