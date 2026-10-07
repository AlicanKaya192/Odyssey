Error situations from real life and the right responses.

## The program froze

**Symptom:** No output; the program never ends.
**Cause:** No `timeout`; the server does not answer and requests waits for
ever.
**Response:** Give every request a value such as `timeout=5`; catch
`requests.Timeout`.

## The overnight script stopped half-way

**Symptom:** It stopped on page 140 of 300 with a `ConnectionError`.
**Cause:** The network dropped for a moment; a single error ended the whole
job.
**Response:** Wrap the page request in a retry function; also save what you
have so far so you do not have to start over (Section 15).

## The server's owner complained

**Symptom:** "You are sending hundreds of requests a second."
**Cause:** On `503` it retried in a loop without waiting.
**Response:** Wait between retries and double the wait; set an upper limit;
follow `Retry-After`.

## The same order was created three times

**Symptom:** Duplicate records in the database.
**Cause:** A `POST` was retried automatically after a timeout; the requests
had in fact reached the server.
**Response:** Do not retry a `POST` automatically. If needed, check with a
`GET` whether the record was created first.

## The error never goes away

**Symptom:** All five attempts got `404`.
**Cause:** A `4xx` is not temporary; waiting changes nothing.
**Response:** Do not retry on `4xx`; fix the address, the identifier or the
body.
