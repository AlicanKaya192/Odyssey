Look here if you get stuck installing. The problems are listed in the
order they usually come up.

## "ODBC driver not found"

Odyssey connects to the server with `ODBC Driver 18 for SQL Server`. This
message says that driver is not installed.

To check: type **ODBC** in the Start menu, open "ODBC Data Sources
(64-bit)", go to the **Drivers** tab. The driver's name should be in the
list.

If it is not, install it from the **x64** link on
<https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server>,
then **close Odyssey and open it again.** A running program does not see
a driver installed underneath it.

## "Cannot reach SQL Server"

The driver is there but the server is not answering. Three possibilities:

**The server is not running.** Type `services.msc` in the Start menu. Find
the **SQL Server (SQLEXPRESS)** row in the list. If the Status column does
not say "Running", right-click the row and choose **Start**.

Double-click the same row and set **Startup type** to **Automatic** and it
will start on its own every time you turn the machine on.

**The instance name is different.** Odyssey tries `.\SQLEXPRESS`,
`(localdb)\MSSQLLocalDB`, `.` and `localhost`. If you chose `Custom`
instead of `Basic` during setup and typed a different name, it will not
find it. The easiest fix is to run the installer again and choose `Basic`.

**The installation did not finish.** If you closed the setup window early,
the service may never have been created. Run the installer again.

## Setup says "a restart is pending"

If Windows has an update waiting, SQL Server setup will not start. Restart
the machine, then run the installer again.

## Setup asks for ".NET Framework"

This comes up on older Windows versions. Install it from the link the
installer gives you, then run setup again.

## SSMS opens but cannot connect

There are three boxes in the SSMS connection window:

- **Server name**: `.\SQLEXPRESS` — the leading dot means "this machine".
- **Authentication**: `Windows Authentication`. It asks for no username or
  password; you sign in with your Windows account.
- **Encryption**: `Optional`. The default is `Mandatory`, which raises a
  certificate error on local installations.

## Odyssey works but SSMS does not (or the other way round)

Both connect to the same server, so if one works the server is up. The
problem is in the other one's settings.

- If only SSMS connects: the ODBC driver is missing.
- If only Odyssey connects: fill in the three boxes of the SSMS connection
  window as above.

## Removing exercise databases

Odyssey creates a database with an `Odyssey_` prefix for each exercise.
There is no situation where you have to delete them; if you would rather
they did not take up space, right-click and delete them in SSMS. Odyssey
will build a new one on the next run.
