`/report` answers correctly, but there's a `time.sleep` inside `async def`:
requests arriving at once queue up.

**What to do:** turn the waiting into a form that doesn't lock the event
loop. The answer stays the same: `{"rows": 120}`.
