Most permission mistakes come from haste, not bad intent: something does
not work, someone widens the permission, the job works and the permission
stays that way. This note collects the most common mistakes and their
correct counterparts.

## "It does not work, let me make it 777"

If a program cannot read a file, the easiest "fix" is to give everyone
every permission. It works, but now everyone on the system can change that
file. The right way is to find **which user** the program runs as and give
only that user (or its group) the permission it needs: `640` or `750` is
usually enough.

## A secret file with a wide permission

Keys, password files and configurations holding secrets such as `.env`
should be `600`. Permissions can change when copying, extracting from an
archive or moving to another computer; that is why the permission of files
holding secrets is checked again after they are moved. How secrets should
be stored is the topic of the Secrets Management section.

## A script anyone can write

If a script run by an administrator or a scheduled task can be written by
anyone, any user can add their own command to the script and that command
runs with the administrator's privilege. Every file that runs with
privilege must be writable only by its owner (and that owner must be
privileged too). This is one of the most common causes of privilege
escalation, the topic of the next section.

## Ownership matters as much as permission

A file with permission `600` is open to the wrong person if its owner is
the wrong user. A check reads the owner and the group along with the
permission.

## Checklist

| Finding | Why is it bad? | Fix |
|---|---|---|
| A file anyone can write (`o+w`) | Anyone can change its contents | `chmod o-w` |
| A file holding secrets readable by the group or others | The secret leaks | `chmod 600` |
| A script run with privilege writable by others | Privilege escalation | Owned by a privileged account, `755` or narrower |
| No sticky bit on a shared folder | Anyone deletes anyone's files | Add the sticky bit |
| An unneeded setuid program | A door to privilege escalation | Remove the setuid bit |

## Automatic checks

Checking permissions one by one by hand does not scale. A script reads the
list of files and their permissions, applies the rules above and reports
the findings. The `audit_files` exercise is a toy version of this idea: it
works on the list it is given, without touching the real file system.
