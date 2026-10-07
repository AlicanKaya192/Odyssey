# Tags and Releases

When you release a program, you want to mark how it looked at that moment:
"version 1.0 that went to users is **this** commit". So that when a bug is
reported you can go back to exactly that code, and see what changed between
two versions.

Git's tool for this is the **tag**: a **permanent** name given to a commit.

## Branch versus tag

Both are names pointing to a commit. The difference:

| | Branch | Tag |
|---|---|---|
| When you commit | Moves on | **Stays put** |
| For | Ongoing work | An important moment in the past (a release) |
| Example | `main`, `login` | `v1.0`, `v2.3.1` |

A tag points to the same commit forever; `v1.0` is always version 1.0.

## Lightweight tag

The simplest: just a name.

```text
~/app (main) $ git tag v1.0
~/app (main) $ git tag
v1.0
~/app (main) $ git log --oneline
6d6d69b (HEAD -> main, tag: v1.0) Fix search bug
e44c10f Add search
25a8f90 Add prototype
```

`git log` now shows `tag: v1.0` next to that commit.

## Annotated tag

The recommended form for releases is the **annotated** tag: who tagged it,
when, and a message. Created with `-a`, message with `-m`:

```text
~/app (main) $ git tag -a v1.1 -m "Search works"
~/app (main) $ git show v1.1 --stat
tag v1.1
Tagger: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:03:00 2026 +0300

Search works

commit 6d6d69be195421861c3a621844b5a374873e9874 (HEAD -> main, tag: v1.1)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:02:00 2026 +0300

    Fix search bug

 app.txt | 1 +
 1 file changed, 1 insertion(+)
```

`git show` first shows the tag's information (tagger, date, message), then the
commit it points to. A lightweight tag doesn't have the first part.

| | Lightweight | Annotated |
|---|---|---|
| Create | `git tag v1.0` | `git tag -a v1.0 -m "..."` |
| Stores | Only the name | Tagger, date, message |
| Use | Personal, temporary markers | Released versions |

## Tagging an old commit

If you forgot to tag, you can do it later; give the commit:

```text
~/app (main) $ git log --oneline
6d6d69b (HEAD -> main, tag: v1.1) Fix search bug
e44c10f Add search
25a8f90 Add prototype
~/app (main) $ git tag v0.1 HEAD~2
~/app (main) $ git tag -n
v0.1            Add prototype
v1.1            Search works
```

`git tag -n` writes each tag's message (the commit message if it isn't
annotated) next to it.

## Listing, deleting

| Command | What it does |
|---|---|
| `git tag` | All tags (alphabetical). |
| `git tag -l "v1.*"` | Those matching a pattern. |
| `git tag -n` | With their messages. |
| `git show v1.0` | The tag and commit in detail. |
| `git tag -d v1.0` | Deletes the tag (doesn't touch the commit). |

A second tag with the same name can't be created; to move one, delete it
first and create it again.

## Pushing tags to GitHub

**`git push` doesn't push tags.** You have to send them separately:

```text
~/app (main) $ git tag -a v1.1 -m "Search works"
~/app (main) $ git push
Everything up-to-date
~/app (main) $ git push origin v1.1
To https://github.com/ada/app.git
 * [new tag]         v1.1 -> v1.1
~/app (main) $ git tag v1.0 HEAD~1
~/app (main) $ git push --tags
To https://github.com/ada/app.git
 * [new tag]         v1.0 -> v1.0
```

| Command | What it does |
|---|---|
| `git push origin v1.1` | Pushes a single tag. |
| `git push --tags` | Pushes all tags. |
| `git push origin --delete v1.1` | Deletes the tag on GitHub. |

> Don't change a pushed tag. If others downloaded `v1.0`, your new `v1.0`
> won't replace theirs; there will be two different "1.0"s. If there is a bug,
> release a new version (`v1.0.1`).

## Version numbers: SemVer

Most projects use **Semantic Versioning**: `MAJOR.MINOR.PATCH`, for example
`2.4.1`.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>MAJOR (2.x.x)</span><span>An incompatible change: users have to change their code.</span></div>
    <div class="anat-row"><span>MINOR (x.4.x)</span><span>A new feature; old usage works as before.</span></div>
    <div class="anat-row"><span>PATCH (x.x.1)</span><span>A bug fix; nothing else changes.</span></div>
  </div>
  <figcaption>When a number goes up, the ones to its right reset: 1.4.2 → 1.5.0 → 2.0.0.</figcaption>
</figure>

The tag name usually gets a leading `v`: `v2.4.1`.

## `git describe`: where am I?

`git describe` describes the commit you are on relative to the nearest
annotated tag:

```text
~/app (main) $ git log --oneline
6d6d69b (HEAD -> main) Fix search bug
e44c10f (tag: v1.1) Add search
25a8f90 Add prototype
~/app (main) $ git describe
v1.1-1-g6d6d69b
~/app (main) $ git checkout v1.1
Note: switching to 'v1.1'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at e44c10f Add search
~/app (e44c10f...) $ git describe
v1.1
~/app (e44c10f...) $ git switch main
Previous HEAD position was e44c10f Add search
Switched to branch 'main'
```

`v1.1-1-g…` means "1 commit after v1.1, I'm at …" (`g` is a prefix meaning
"git"). It is used to print a program's version automatically. `--tags` also
counts lightweight tags.

## Switching to a tag

`git switch` won't go to a tag (a tag isn't a branch); `git checkout v1.0` does,
but HEAD becomes **detached**: you are on no branch. Fine for looking at an
old version; if you'll work there, create a branch (`git switch -c fix-1.0
v1.0`). More on detached HEAD in 14.

## A release on GitHub

GitHub's **Releases** page is built on tags: you pick a tag, write a title and
release notes, and attach downloadable files (like an installer). Users
download the program from there. (This program's updates are published the
same way.)

## Summary

- A tag is a permanent name for a commit; it doesn't move like a branch.
- Lightweight: `git tag v1.0`. Annotated (for releases): `git tag -a v1.0 -m
  "..."`.
- An old commit: `git tag v0.9 <commit>`; deleting is `git tag -d`.
- Tags are pushed separately: `git push origin v1.0` or `--tags`.
- SemVer: MAJOR (incompatible) . MINOR (new feature) . PATCH (fix).
- `git describe` gives the position relative to the nearest tag; switching to a
  tag detaches HEAD.
