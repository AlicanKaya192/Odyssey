`hostname_of(url)` should return the name of the server an address goes
to, in lower case; empty text if there is none.

The starter code splits the address at `/`. It gives the wrong result for
addresses with a user name such as `school.example@evil.test` or with a
port such as `:8443`. Use `urllib.parse.urlsplit(url).hostname`; it
separates both the user name and the port and also turns the name into
lower case.

**Expected output:**

```
login.school.example
evil.test
files.example
login.school.example
```
