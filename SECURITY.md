<div align="right">
  <a href="./SECURITY.tr.md">Türkçe</a> · <b>English</b>
</div>

# Security Policy

## Supported Versions

The project is in early development. Security reports are always evaluated
against the **current state of the `main` branch** and the **latest published
release**.

| Version | Supported |
|---|:-:|
| `main` (development) | ✅ |
| Latest published release | ✅ |
| Older releases | ❌ |

## The application's security surface

This is a desktop application, not a service. What you should know:

**No server, no account, no telemetry.** Your progress, your profile and the
code you write stay on your own computer, in `%APPDATA%\Odyssey\progress.db`.
No data is sent anywhere.

**The application currently makes no network calls at all.** The update check
planned for a later version will be switchable from Settings.

Addresses in the "My Links" and "Extra Content" tabs do not open inside the
application; clicking one hands it to the system browser.

**The application runs Python code written by the user.** That is the design
itself — it is how exercises are checked. But it needs to be stated plainly:

> **This is not a security sandbox.** Users run their own code on their own
> machine. What the system provides is an isolated working folder, a timeout,
> an output limit, and the guarantee that the application does not crash when
> the code raises an error. It will not stop malicious code.

For that reason, **do not add exercise content from someone else without
reviewing it first.** A `solution.py` or a data file placed under `content/`
runs with your privileges when the exercise is run.

## Reporting a vulnerability

Findings of the following kinds count as vulnerabilities and reports are
appreciated:

- An API key, token or credential accidentally left in the code
- User data leaving the application in an unexpected way
- The application connecting to a network address without the user asking
- The exercise runner running with more privileges than it needs, or writing
  outside its isolated working folder
- A known vulnerability in a dependency that directly affects this project
- The update mechanism loading unverified content

**These do not count as vulnerabilities:** user-written code being able to
reach the user's own files (that is by design), and code with an infinite loop
consuming CPU (it is stopped by the timeout).

### How to report

**Do not post the vulnerability in a public issue.** Instead:

1. Open a private report through GitHub's
   [Security Advisories](https://github.com/AlicanKaya192/Odyssey/security/advisories/new),
   or
2. Write to one of the contact addresses on
   [my GitHub profile](https://github.com/AlicanKaya192).

The review goes faster if the report includes: the affected version,
step-by-step reproduction, the likely impact, and an idea for a fix if you
have one.

### Process

- I confirm receipt of the report **within 48 hours**.
- **Within 7 days** I report whether the issue is valid and what its impact is.
- If it is valid, I keep you informed until a fix is released.
- When the fix ships, I credit you in the release notes if you would like that.

The project is run by one person on a voluntary basis; these timelines are
good-faith targets, not commitments.
