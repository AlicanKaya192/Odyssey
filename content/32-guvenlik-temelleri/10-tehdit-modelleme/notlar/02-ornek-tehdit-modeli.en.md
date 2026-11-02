A small threat model for the login flow of the school grades system. The
parts: the student (external entity), the login request (data flow,
crossing the trust boundary), the web application (process), the user
table and the log file (data stores).

| Part | Letter | What could happen? | Answer |
|---|---|---|---|
| Student | S | Logging in with someone else's password | MFA, limit on tries |
| Student | R | Saying "I didn't log in" | A login log: time, source, result |
| Login request | T | The password being changed on the way | HTTPS only |
| Login request | I | The password being read on the way | HTTPS only |
| Login request | D | The page being locked up with many requests | Rate limit per source |
| Web application | S | The application presenting itself as another service | Authentication between services |
| Web application | T | Session data being changed | A signed session token |
| Web application | I | An error message saying whether the user exists | One uniform error message |
| Web application | E | A student using the teacher page | A role check on the server |
| User table | T | Password hashes being changed | Least privilege for the application user |
| User table | I | The table leaking | A salted, slow hash |
| Log file | R | Wiping traces by deleting the logs | Copying logs to another system |
| Log file | I | Passwords showing up in the logs | Never writing passwords to the log |

## What comes out of this table

- The same control can close several rows (HTTPS for both T and I).
- Some rows link to other sections: storing passwords, authorization,
  error messages. A threat model is a map of the work to be done.
- If every row has an owner and a date, the table becomes a to-do list.
- Some rows can be scored and accepted; what matters is that the decision
  is written down.
