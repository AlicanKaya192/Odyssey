You do not need SSMS for the exercises, but everyone who writes SQL for a
living has it open on screen. This note is a short tour: what sits where.

## Connecting

The first window when the program opens is the connection window:

| Box | What to put |
|---|---|
| Server type | `Database Engine` |
| Server name | `.\SQLEXPRESS` |
| Authentication | `Windows Authentication` |
| Encryption | `Optional` |

Press **Connect**, the window closes and a tree appears on the left. You
are connected.

## The tree on the left: Object Explorer

Everything inside the server lives here. This is what you see:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Databases</span><span class="anat-body">The databases on the server. Odyssey's exercise databases (prefixed <code>Odyssey_</code>) show up here.</span></div>
    <div class="anat-row"><span class="anat-label">System Databases</span><span class="anat-body">The four databases SQL Server keeps for its own work: <code>master</code>, <code>model</code>, <code>msdb</code>, <code>tempdb</code>. We leave these alone.</span></div>
    <div class="anat-row"><span class="anat-label">Security</span><span class="anat-body">Users and permissions.</span></div>
    <div class="anat-row"><span class="anat-label">Server Objects</span><span class="anat-body">Backup targets, linked servers. Advanced topics.</span></div>
  </div>
</figure>

Open a database and you see **Tables** underneath; open that and the
tables are listed. Under a table, **Columns** shows the columns and their
types — the fastest way to learn what a table looks like.

## Looking at a table

Right-click a table and choose **Select Top 1000 Rows** and SSMS writes
the query for you and shows the result. In the early days this is very
useful for getting to know a table.

## Writing a query

The **New Query** button at the top opens an empty query tab.

**F5** runs what you wrote. Select part of the text and press F5 and
**only the selection** runs — that is how you try one query out of a long
file.

The dropdown at the top shows which database the tab is attached to. When
you are on the wrong database you get "no such table"; that is the first
place to look.

## What is `GO`?

In scripts written in SSMS you will see `GO` on a line of its own. It is
**not SQL**; it is SSMS's "send everything up to here" command. The server
knows nothing about `GO`.

Odyssey reads `GO` lines the same way, so a script you copied out of SSMS
runs as it is.

## Shortcuts

| Key | What it does |
|---|---|
| `F5` | Run |
| `Ctrl + N` | New query tab |
| `Ctrl + Shift + R` | Refresh the completion list (when a new table does not show) |
| `Ctrl + K, Ctrl + C` | Comment out the selected lines |
| `Ctrl + K, Ctrl + U` | Uncomment |
