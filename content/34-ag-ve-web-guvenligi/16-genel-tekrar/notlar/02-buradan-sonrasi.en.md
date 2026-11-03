This module covered how requests are protected on the network and the
common weaknesses of web applications. The path's last module looks at the
systems behind them and at day-to-day operation.

## System Security and Operations

- **Memory and the operating system:** how a program's memory gets
  corrupted and how the operating system limits that; file permissions and
  privilege escalation. The "least-privileged database user" idea from
  here is applied to operating system accounts there.
- **Secure software development:** how this module's defences
  (parameterised queries, encoding, allow lists) become a habit in a team
  through code review and dependency checks.
- **Secret management:** where API keys, signing secrets and the session
  signing key go instead of the code, and how they are renewed.
- **Logging, monitoring and incident response:** the "monitoring per
  source" from the Authentication Failures section and OWASP's logging
  category turn into intrusion detection there, and then into an incident
  response plan.

## While studying

- In your own small web projects, apply this section's "path of a
  request" order: session, origin and token, ownership, a parameterised
  query, encoded output.
- In the browser's developer tools, look at your own site's response
  headers and cookie attributes; compare them with the Header Template
  note.
- Use OWASP's web and API lists and its Cheat Sheet Series as a
  reference; the lists are updated every few years.
- Try the techniques you learn only on your own systems or in practice
  environments where it is explicitly allowed. Testing without permission
  is a crime.
