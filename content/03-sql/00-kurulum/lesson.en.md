# Installing SQL Server

On this path you will learn SQL on a **real database server**, not behind
a Python library. You write the query, the server runs it, the result
table comes back. This is exactly how the work is done in companies.

This section does one thing: **it sets up the machinery.** By the end you
will press Run and see a result. Everything else comes after that.

## Why Microsoft SQL Server?

SQL is a language, but there is no single SQL. Every database speaks its
own dialect: PostgreSQL, MySQL, Oracle, SQL Server. The core — `SELECT`,
`WHERE`, `JOIN` — is the same everywhere; the differences sit at the
edges.

The reason we picked Microsoft SQL Server is simple: **it is the one you
are most likely to meet in a company.** Banks, insurers, public sector,
the back end of ERP systems — usually it is sitting there. Its dialect is
called **T-SQL**.

And if you later need a different one, nothing is wasted: 90% of what you
know carries over unchanged.

The edition you will install is **Express** — the one Microsoft
distributes at no charge. It has a size limit (10 GB per database) but it
supports the whole language; nothing is missing for learning.

## First, let us separate the things people confuse

You will see four different names during the installation. If you know
which is which up front, the installation gets easier:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SQL Server</span><span class="anat-body">The server itself. A <b>service running in the background</b> on your machine; no window, no icon. This is the thing that holds the data and runs the queries.</span></div>
    <div class="anat-row"><span class="anat-label">Database</span><span class="anat-body">A box inside the server. One server can hold dozens of databases; tables live inside them.</span></div>
    <div class="anat-row"><span class="anat-label">T-SQL</span><span class="anat-body">The dialect SQL Server speaks. This is the language you will write.</span></div>
    <div class="anat-row"><span class="anat-label">SSMS</span><span class="anat-body">A <b>client program</b> that connects to the server (SQL Server Management Studio). Not the server, just the window you look through.</span></div>
    <div class="anat-row"><span class="anat-label">ODBC driver</span><span class="anat-body">The layer programs use to talk to the server. Odyssey uses it too.</span></div>
  </div>
  <figcaption>The most common mix-up: installing SSMS and thinking you have installed SQL Server. SSMS is only a window; with no server behind it, it opens onto nothing.</figcaption>
</figure>

## How Odyssey connects

When you press Run, this is what happens:

<figure class="fig">
  <div class="flow">
    <span class="node">Your query</span>
    <span class="arrow">-&gt;</span>
    <span class="node">Odyssey</span>
    <span class="arrow">-&gt;</span>
    <span class="node">ODBC Driver 18</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">SQL Server</span>
    <span class="arrow">-&gt;</span>
    <span class="node ok">Result table</span>
  </div>
  <figcaption>Every link in the chain is needed. The next steps install the first three; the last one comes for free.</figcaption>
</figure>

Odyssey **finds the server itself**; you do not type an address. It tries
`.\SQLEXPRESS`, `(localdb)\MSSQLLocalDB`, `.` and `localhost` in turn and
uses whichever answers.

## Step 1 — SQL Server Express

Download page: **<https://go.microsoft.com/fwlink/p/?linkid=2216019>**

That address is Microsoft's **own forwarding link**: when a new version
ships, Microsoft repoints it, so you always get the current one. If it
does not work, go to
<https://www.microsoft.com/en-us/sql-server/sql-server-downloads>
and find the "Express" heading.

Run the file you downloaded and three options appear. Pick **Basic** —
the other two are for enterprise setups and you do not need them.

The rest goes on its own: accept the licence text, leave the folder as
it is, wait for it to finish. It takes five to fifteen minutes.

The final screen shows a few details. Check that **Instance Name** reads
`SQLEXPRESS`, then close the window. You do not need the other buttons
("Connect Now", "Customize", "Install SSMS").

Once the installation finishes the server is **already running**, and it
starts on its own every time you turn the machine on. There is nothing
else to launch.

## Step 2 — the ODBC driver

This is how Odyssey connects to the server. It usually gets installed
along with step 1, so you probably already have it.

To check: type **ODBC** in the Start menu, open "ODBC Data Sources
(64-bit)", go to the **Drivers** tab. `ODBC Driver 18 for SQL Server`
should be in the list.

If it is not, install it from
<https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server>
— take the **x64** link on that page.

## Step 3 — SSMS (optional)

**<https://aka.ms/ssmsfullsetup>** — this address always gives the
current version too.

SSMS lets you connect to the server, browse databases as a tree, open
tables by clicking them and write queries. Everyone who writes SQL for a
living has it open on screen.

**You do not need it for the exercises.** You will write and run queries
inside Odyssey. But at some point you will want to see the work in a real
tool, and SSMS is that tool. Skipping it now is fine; install it later.

When SSMS opens, a connection window appears. Put `.\SQLEXPRESS` in
**Server name**, pick `Windows Authentication` under **Authentication**
and `Optional` under **Encryption**, then press Connect.

## Step 4 — try it

The setup is done. Now see it work: go to the **Exercise** tab of this
section and press **Run**.

If a table appears in the result panel, the whole chain is working.

## If nothing happens

Whatever the error message says, the cause is usually one of two things:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">"ODBC driver not found"</span><span class="anat-body">Step 2 is missing. Install the driver, then restart Odyssey.</span></div>
    <div class="anat-row"><span class="anat-label">"Cannot reach SQL Server"</span><span class="anat-body">The server may not be running. Type <code>services.msc</code> in the Start menu, find the <b>SQL Server (SQLEXPRESS)</b> row; if its status is not "Running", right-click and start it.</span></div>
  </div>
</figure>

If you changed the instance name during setup (typed something other than
`SQLEXPRESS`), Odyssey will not find it. The easiest fix is to run the
installer again and choose `Basic`.

## Nothing happens to your data

After this section you will build databases of your own. Two things so
you know Odyssey's exercises do not touch them:

- Exercise databases are created with an **`Odyssey_` prefix**. They stay
  out of the way of your own databases.
- Every time you run an exercise, **every change you made is rolled
  back.** Even if you drop a table by accident, it is there again on the
  next run. This is deliberate: we do not want you to be afraid to try
  things.

## Summary

- **SQL Server** is the background server, **SSMS** is a window onto it,
  the **ODBC driver** is how programs connect. Three different things.
- Install the **Express** edition, choose **Basic**, instance name
  **SQLEXPRESS**.
- Odyssey finds the server itself; you do not type an address.
- SSMS is not required for the exercises, but it is the tool used in the
  field.
- Everything you write is rolled back at the end of a run; do not be
  afraid to break things.
