The best time to deal with SSRF is when **designing** a feature that takes
an address. The questions below are asked before the feature is written
(Insecure Design, the OWASP Top 10 section).

## Design questions

1. **Does the user really need to give an address?** Often not: the user
   can upload the file themselves or pick from a list. A feature that takes
   no address has no SSRF.
2. **Which sites must be reached?** If it is a few specific sites, build an
   allow list. If it must be "anywhere", rejecting internal addresses and
   limiting the network are a must.
3. **Which schemes?** Only `http` and `https`.
4. **Which ports?** Usually only 80 and 443; another port may be an
   internal service.
5. **What will be done with the response?** Only the expected type (an
   image, a specific JSON) and up to a certain size. The raw response is
   not shown to the user.
6. **What does the user see on an error?** A general message. Even the
   difference between "connection refused" and "timeout" can reveal which
   addresses exist on the internal network.

## Order of implementation

1. Parse the address with `urlsplit`; check the scheme and port.
2. Compare the host with the allow list (if there is one).
3. Resolve the name; check **every** resulting IP address with the
   internal-address rule.
4. Open the connection to the checked IP; a short timeout.
5. Do not follow redirects, or repeat 1–4 at every step.
6. Check the response's type and size.

## Common mistakes

- Checking with `startswith("https://images.example.com")`.
- Checking the name but not the IP.
- Blindly following redirects.
- Switching off authentication in internal services because "this server
  is inside anyway, so it is safe".
- Showing the internal server's response in an error message.
