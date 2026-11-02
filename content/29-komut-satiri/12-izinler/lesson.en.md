# Permissions and chmod

Linux is a multi-user system: several people, a web server and a database can
all run on the same computer. **Permissions** decide who may read, change and
run which file. You meet them every day on your own computer too: the first
time you run a script you wrote, you will most likely see `Permission denied`.

## Reading permissions

In the Looking Closer with ls section we left the permissions column for this
section. Now its turn has come:

```text
~ $ ls -l notes.txt scripts/hello.sh
-rw-r--r-- 1 ada ada  9 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada 37 Oct  7 10:00 scripts/hello.sh
~ $ ls -ld private
drwxr-xr-x 2 ada ada 4096 Oct  7 10:00 private/
~ $ whoami
ada
~ $ id
uid=1000(ada) gid=1000(ada) groups=1000(ada)
```

<figure class="fig">
  <pre><code class="language-text">-rwxr-xr-- 1 ada ada 37 Oct  7 10:00 hello.sh</code></pre>
  <div class="anat">
    <div class="anat-row"><span>-</span><span>Type: <code>-</code> a file, <code>d</code> a folder.</span></div>
    <div class="anat-row"><span>rwx</span><span>The <b>owner</b> (user, <code>u</code>): reads, writes, runs.</span></div>
    <div class="anat-row"><span>r-x</span><span>The <b>group</b> (<code>g</code>): reads and runs; cannot write.</span></div>
    <div class="anat-row"><span>r--</span><span><b>Others</b> (<code>o</code>): read only.</span></div>
    <div class="anat-row"><span>ada ada</span><span>The owning user and group.</span></div>
  </div>
  <figcaption>The nine letters are three groups of three. A <code>-</code> instead of a letter means that permission is missing.</figcaption>
</figure>

- There are three permissions: **r** read, **w** write, **x** execute.
- There are three groups of people: the **owner** (`u`, *user*), the **group**
  (`g`) and **others** (`o`).
- `whoami` tells you who you are, `id` which groups you are in. In this
  terminal you are `ada` and the files belong to `ada`, so the first triple is
  the one that concerns you.

`rw-r--r--` for `notes.txt`: you read and write, the others only read. A new
file always starts like this; a new folder with `rwxr-xr-x`.

## Execute permission: `+x`

```text
~ $ ./scripts/hello.sh
bash: ./scripts/hello.sh: Permission denied
~ $ echo $?
126
~ $ bash scripts/hello.sh
Hello from a script
~ $ chmod +x scripts/hello.sh
~ $ ls -l scripts/hello.sh
-rwxr-xr-x 1 ada ada 37 Oct  7 10:00 scripts/hello.sh*
~ $ ./scripts/hello.sh
Hello from a script
~ $ ls scripts
hello.sh*
```

- `./scripts/hello.sh` runs a script **as a program**, and that needs `x`. The
  shell returned exit code `126`: "found it but cannot run it".
- `bash scripts/hello.sh` works, though: the program running here is `bash`,
  which only **reads** the script; `r` is enough.
- `chmod +x` added the execute permission; `ls` now puts a `*` after the name.

Writing scripts is the next section's topic; every script there will start
with this step.

## Changing with letters

`chmod` (*change mode*) is read like this: **who**, **what to do**, **which
permission**.

| Who | Operation | Permission |
|---|---|---|
| `u` owner | `+` add | `r` |
| `g` group | `-` remove | `w` |
| `o` others | `=` exactly this | `x` |
| `a` all | | |

```text
~ $ chmod u-w notes.txt
~ $ ls -l notes.txt
-r--r--r-- 1 ada ada 9 Oct  7 10:00 notes.txt
~ $ echo Call Ada >> notes.txt
bash: notes.txt: Permission denied
~ $ chmod u+w notes.txt
~ $ chmod go-r notes.txt
~ $ ls -l notes.txt
-rw------- 1 ada ada 9 Oct  7 10:00 notes.txt
~ $ chmod g+w,o+r shared.txt
~ $ ls -l shared.txt
-rw-rw-r-- 1 ada ada 10 Oct  7 10:00 shared.txt
~ $ chmod a-w shared.txt
~ $ ls -l shared.txt
-r--r--r-- 1 ada ada 10 Oct  7 10:00 shared.txt
```

- `u-w` removed writing from the owner; `>>` can no longer add to the file. The
  shell printed the error, because the shell was the one trying to open the
  file.
- `go-r` removed reading from the group and others: the file is yours only.
- Several changes with commas: `g+w,o+r`.
- `a-w` removes writing from everyone. If no who is given (like `+x`),
  everyone is meant.

## Changing with numbers

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>r = 4</span><span>Read</span></div>
    <div class="anat-row"><span>w = 2</span><span>Write</span></div>
    <div class="anat-row"><span>x = 1</span><span>Execute</span></div>
    <div class="anat-row"><span>7 = 4+2+1</span><span><code>rwx</code></span></div>
    <div class="anat-row"><span>6 = 4+2</span><span><code>rw-</code></span></div>
    <div class="anat-row"><span>5 = 4+1</span><span><code>r-x</code></span></div>
    <div class="anat-row"><span>4</span><span><code>r--</code></span></div>
    <div class="anat-row"><span>0</span><span><code>---</code></span></div>
  </div>
  <figcaption>Each group is one digit: owner, group, others. <code>755</code> = <code>rwxr-xr-x</code>, <code>644</code> = <code>rw-r--r--</code>, <code>600</code> = <code>rw-------</code>.</figcaption>
</figure>

```text
~ $ chmod 600 notes.txt
~ $ ls -l notes.txt
-rw------- 1 ada ada 9 Oct  7 10:00 notes.txt
~ $ chmod 755 scripts/hello.sh
~ $ ls -l scripts/hello.sh
-rwxr-xr-x 1 ada ada 37 Oct  7 10:00 scripts/hello.sh*
~ $ chmod 444 shared.txt
~ $ ls -l shared.txt
-r--r--r-- 1 ada ada 10 Oct  7 10:00 shared.txt
~ $ chmod 644 notes.txt shared.txt
~ $ ls -l notes.txt shared.txt
-rw-r--r-- 1 ada ada  9 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada 10 Oct  7 10:00 shared.txt
```

A number writes every triple **from scratch**; letters change only the
permission you name. `+x` is handy for "add execute to a file", a number for
"this file's permission must be exactly this". Three numbers worth learning by
heart: `644` a regular file, `755` a program or folder, `600` a file that is
yours only.

`chmod 777` (everyone does everything) looks like a quick fix, but it lets
anyone change and run your file. Always give the **least** permission the job
needs.

## Permissions on folders

On a folder the letters mean slightly different things:

- `r`: listing what is inside (`ls`).
- `w`: creating, deleting and renaming files in it.
- `x`: entering it (`cd`) and **reaching** the files inside.

```text
~ $ chmod 700 private
~ $ ls -ld private
drwx------ 2 ada ada 4096 Oct  7 10:00 private/
~ $ chmod u-x private
~ $ cd private
bash: cd: private: Permission denied
~ $ cat private/secret.txt
cat: private/secret.txt: Permission denied
~ $ chmod u+x private
~ $ cat private/secret.txt
the plan
```

Once `x` was gone, not only `cd` but also reading the file inside was refused,
even though the file's own permission is `rw-r--r--`. Every folder on the way
to a file needs `x`.

## System files and root

```text
~ $ ls -l /etc/passwd
-rw-r--r-- 1 root root 129 Oct  7 10:00 /etc/passwd
~ $ ls -ld /root /tmp
drwx------ 2 root root 4096 Oct  7 10:00 /root/
drwxrwxrwt 2 root root 4096 Oct  7 10:00 /tmp/
~ $ cd /root
bash: cd: /root: Permission denied
~ $ touch /etc/test.txt
touch: cannot touch '/etc/test.txt': Permission denied
~ $ touch /tmp/test.txt
~ $ ls -l /tmp/test.txt
-rw-r--r-- 1 ada ada 0 Oct  7 10:00 /tmp/test.txt
```

The system's own files belong to an administrator called **root**. Anyone can
read `/etc/passwd` but only root can change it; `/root` is root's home folder
and completely closed to everyone else. `/tmp` is a temporary folder open to
everyone (the `t` at the end means that everyone can delete only their own
files there).

On a real Linux system you write `sudo` in front of a command that needs
administrator rights: `sudo touch /etc/test.txt`. sudo asks for your password
and runs the command as root. This terminal has no `sudo`; the details are in
the lesson notes.

## Traps

```text
~ $ chmod abc notes.txt
chmod: invalid mode: 'abc'
Try 'chmod --help' for more information.
~ $ chmod 999 notes.txt
chmod: invalid mode: '999'
Try 'chmod --help' for more information.
~ $ chmod +x
chmod: missing operand after '+x'
Try 'chmod --help' for more information.
~ $ chmod 000 notes.txt
~ $ cat notes.txt
cat: notes.txt: Permission denied
~ $ chmod 644 notes.txt
```

- An invalid permission gives `invalid mode`; the digits go from 0 to 7.
- If you forget the file name: `missing operand`.
- `chmod 000` closes the file even to its owner; but the owner can give the
  permission back.

## Summary

| Command | What it does |
|---|---|
| `ls -l`, `ls -ld folder` | Shows the permissions |
| `chmod +x f` | Adds execute permission |
| `chmod u-w f` | Removes writing from the owner |
| `chmod go-r f` | Removes reading from the group and others |
| `chmod 644 f` | `rw-r--r--` |
| `chmod 755 f` | `rwxr-xr-x` |
| `chmod 600 f` | `rw-------` |
| `chmod 700 folder` | Only the owner can enter |

r = 4, w = 2, x = 1; the digits are owner, group, others in that order.
