`mask(text)` should apply each rule in `MASKS` **in order**
(`re.sub(pattern, placeholder, text)`), then lowercase the text and collapse
spaces into one.

**Expected output:**

```
refund amount for ordernum by date !
error errcode for email
```
