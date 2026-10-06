**English** | [Türkçe](CODE_SIGNING.tr.md)

# Code signing policy

Odyssey's Windows installers and program files are to be code-signed so
that Windows can tell who published them. We have applied to the
[SignPath Foundation](https://signpath.org) programme, which signs open
source projects free of charge. Until the project is approved, releases
are **not signed**, and Windows may show "Windows protected your PC" or
Smart App Control may block the installer.

Once approved:

> Free code signing provided by [SignPath.io](https://about.signpath.io),
> certificate by [SignPath Foundation](https://signpath.org).

The certificate is issued to SignPath Foundation, so Windows shows
**SignPath Foundation** as the publisher.

## What gets signed

Only files built from this repository's public source, on GitHub's
servers, by the [release workflow](.github/workflows/release.yml):

1. The packaged application: `Odyssey.exe` and the executable files
   (`.dll`, `.pyd`) inside it.
2. The installers built from those signed files:
   `Odyssey-X.Y.Z-setup.exe` and the patch installers
   `Odyssey-X.Y.Z-patch-A.B.C.exe`.

Nothing built on a personal computer is signed. Every signing request is
approved by hand before the signature is applied.

## Team and roles

| Role | Who | What it means |
|---|---|---|
| Author | [Alican Kaya](https://github.com/AlicanKaya192) | Writes and changes the source directly. |
| Reviewer | [Alican Kaya](https://github.com/AlicanKaya192) | Reviews every outside contribution (pull request) before it is merged. |
| Approver | [Alican Kaya](https://github.com/AlicanKaya192) | Approves each signing request for a release. |

All team members use multi-factor authentication on GitHub and SignPath.

## Privacy

Odyssey runs offline. Your progress, code, notes and settings stay in
`%APPDATA%\Odyssey` on your computer and are never uploaded. There is no
telemetry, no account and no server of our own.

The program connects to the network only for the following, and sends no
personal data in any of them:

- **Update check.** At startup (and every three hours while it is open)
  it asks GitHub (`api.github.com`) whether a new version has been
  released, and shows the repository's star count. Turned off in
  Settings › Updates; with it off, the program makes neither request.
- **Downloading an update,** only after you press **Update**, from
  GitHub's release page.
- **Discord status.** If the Discord desktop app is running, Odyssey shows
  which screen or section you are on in your Discord status, through the
  Discord app on your computer. The titles and contents of your notes are
  never sent. Turned off in Settings › Appearance.
- **Links you click** open in your own web browser.

The SQL exercises connect to the SQL Server instance on your own computer,
not to the internet.
