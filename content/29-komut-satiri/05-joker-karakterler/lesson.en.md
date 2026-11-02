# Wildcards

Imagine a folder with 200 photos that you want to move to another folder.
Typing the names one by one would take hours. **Wildcards** let you write a
**pattern**: "every file whose name ends in `.jpg`". The shell turns the
pattern into the list of matching names, and the command works on that list.

## Three wildcards and a shorthand

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>*</span><span>Any number of any characters (none is fine too). <code>*.txt</code>: every name ending in .txt.</span></div>
    <div class="anat-row"><span>?</span><span>Exactly <b>one</b> character. <code>photo?.jpg</code>: photo1.jpg yes, photo10.jpg no.</span></div>
    <div class="anat-row"><span>[abc]</span><span><b>One</b> of the characters in the brackets. <code>[0-9]</code> a digit, <code>[a-z]</code> a lower-case letter.</span></div>
    <div class="anat-row"><span>{a,b}</span><span>Not a wildcard but a shorthand: each item in the list is written out, whether a file exists or not.</span></div>
  </div>
  <figcaption>The first three match existing file names; braces are always expanded.</figcaption>
</figure>

## The star: `*`

`*` matches any number of any characters; it can also be none:

```text
~/work $ ls
data.csv  notes.txt  photo1.jpg  photo10.jpg  photo2.jpg  report.txt
~/work $ ls *.txt
notes.txt  report.txt
~/work $ ls photo*
photo1.jpg  photo10.jpg  photo2.jpg
~/work $ echo *.txt
notes.txt report.txt
~/work $ echo *
data.csv notes.txt photo1.jpg photo10.jpg photo2.jpg report.txt
```

- `*.txt`: every name ending in `.txt`.
- `photo*`: every name starting with `photo`.
- `*`: every name in the folder (except hidden ones; more on that soon).

`echo *.txt` wrote the names on one line. This is the easiest way to see how
a wildcard is expanded.

## The shell expands wildcards

The most important idea of this section: wildcards are not expanded by `ls`
or `rm`, they are expanded by **the shell**. The command never sees the star;
it sees the list of names the shell found.

<figure class="fig">
  <div class="flow">
    <span class="node">You type<br><small><code>ls *.txt</code></small></span><span class="arrow">→</span>
    <span class="node acc">The shell expands<br><small>finds the matching names</small></span><span class="arrow">→</span>
    <span class="node">The program sees<br><small><code>ls notes.txt report.txt</code></small></span>
  </div>
  <figcaption>Wildcards are expanded by the shell, not by the programs. <code>ls</code> never sees the star; it sees the list of names.</figcaption>
</figure>

That is why wildcards work with **every** command: `ls`, `cp`, `mv`, `rm`,
`cat`, even `echo`. And that is why looking first with `echo` is safe: `echo`
touches no file, it only prints the list the shell produced.

## The question mark: `?`

`?` matches **exactly one** character:

```text
~/work $ ls photo?.jpg
photo1.jpg  photo2.jpg
~/work $ ls photo??.jpg
photo10.jpg
```

`photo?.jpg` did not take the two-digit `photo10.jpg`; two question marks took
only that one. An easy way to separate single and double digits in numbered
files.

## Square brackets: `[...]`

`[...]` matches **one** of the characters inside. A range is written with a
dash: `[0-9]` a digit, `[a-z]` a lower-case letter.

```text
~/work $ ls photo[12].jpg
photo1.jpg  photo2.jpg
~/work $ ls [dn]*
data.csv  notes.txt
~/work $ ls photo[0-9].jpg
photo1.jpg  photo2.jpg
```

## When nothing matches

```text
~/work $ ls *.pdf
ls: cannot access '*.pdf': No such file or directory
~/work $ echo *.pdf
*.pdf
```

If bash finds no matching name, it leaves the pattern **as it is**. So `ls`
really looked for a file called `*.pdf` and did not find it. `echo` answers
the question "did my pattern match anything?" immediately.

## Turning a wildcard off

Sometimes you want to write the star literally (in a piece of text, for
example). You put it in quotes or put a backslash in front of it:

```text
~/work $ echo "*.txt"
*.txt
~/work $ echo '*.txt'
*.txt
~/work $ echo \*.txt
*.txt
~/work $ echo *.txt
notes.txt report.txt
```

Wildcards are not expanded inside quotes. We will use this a lot with `find`
and `grep` later: we quote the pattern so that the program interprets it, not
the shell.

## Hidden files do not match

`*` and `?` do not match the **dot** at the start of a name. `.hidden.txt` was
not in the output of `echo *`. This is a safety feature: `rm *` does not
touch settings files. If you want hidden files, you write the dot
explicitly: `.h*`.

## Braces: `{a,b}` and `{1..5}`

Braces are not a wildcard but a **shorthand**: they produce one word for each
item in the list. They do not check whether files exist; that is why they are
useful when creating **new** things:

```text
~ $ echo file{1,2,3}.txt
file1.txt file2.txt file3.txt
~ $ echo {a..e}
a b c d e
~ $ mkdir -p site/{css,js,img}
~ $ ls site
css/  img/  js/
~ $ touch site/js/app{1..3}.js
~ $ ls site/js
app1.js  app2.js  app3.js
```

- `{1,2,3}` is a comma-separated list; there is **no space** after the commas.
- `{1..3}` and `{a..e}` are ranges.
- `mkdir -p site/{css,js,img}` created three folders in one command.

## Wildcards and `rm`: look first

A wildcard covers many files with a few characters; combined with `rm`, one
wrong character takes a lot with it. The habit is: try the same pattern with
a harmless command first, then type the real one.

```text
~/work $ ls
a.tmp  data.csv   photo1.jpg   photo2.jpg
b.tmp  notes.txt  photo10.jpg  report.txt
~/work $ echo rm *.tmp
rm a.tmp b.tmp
~/work $ rm *.tmp
~/work $ ls
data.csv  notes.txt  photo1.jpg  photo10.jpg  photo2.jpg  report.txt
```

`echo rm *.tmp` deleted nothing; it only showed the command that would run.
Another common disaster is a space: `rm * .tmp` (a space after the star)
means "delete everything, and a file named `.tmp`".

## Summary

- `*` any number of characters, `?` exactly one character, `[abc]` one from
  the list, `[0-9]` one from the range.
- **The shell** expands wildcards; the command sees the list of names. See
  the result beforehand with `echo pattern`.
- If nothing matches, the pattern stays as it is.
- Quotes or `\` turn a wildcard off.
- Hidden files do not match `*`.
- `{a,b}` and `{1..5}` produce a list without looking at files; handy for
  creating new folders and files.
- Before using a wildcard with `rm`, look at the same pattern with `echo` or
  `ls`.
