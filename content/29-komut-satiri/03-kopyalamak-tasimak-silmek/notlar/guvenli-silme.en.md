`rm` cannot be undone. Experienced users delete the wrong file too; the
difference is a few habits that prevent it.

## Before deleting

1. **Where are you?** `pwd`. A relative path works from the folder you are
   in; in the wrong folder `rm -r tmp` deletes a different `tmp`.
2. **What will you delete?** First `ls` with the same path:
   `ls project/cache`. If you want to delete the list you see, type `rm -r`
   instead of `ls`.
3. **Is it important?** Back it up: `cp -r project project-backup`.

## Options

| Option | When |
|---|---|
| `-i` | When you are not sure: asks for each file |
| `-r` | Only when deleting a folder |
| `-f` | Only in scripts, when you know what you are doing |

`-rf` together means "with contents, without asking, without objecting". The
most common disasters happen with these two letters.

## Dangerous spellings

| Spelling | Why it is dangerous |
|---|---|
| `rm -rf /` | The root folder; this terminal and modern Linux refuse it |
| `rm -rf ~` | Your whole home folder |
| `rm -rf project /` | A stray space: first `project`, then `/` |
| `rm -r *` | Everything in the current folder (see the wildcards section) |

## There is no recycle bin

A file deleted in the terminal does not go to the recycle bin. Desktop
environments have separate tools that send files to the bin (like
`gio trash`), but `rm` is not one of them.
