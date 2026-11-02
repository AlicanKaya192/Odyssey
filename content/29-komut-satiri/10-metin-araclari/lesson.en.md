# Text Tools: sort, uniq, cut, tr

grep chose lines. The four tools in this section **process** lines: they sort
them, count repeats, cut them into pieces and change characters. Alone each
does a small job; joined inside a pipeline they let you summarise a table or a
log file in a few seconds.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>sort</span><span><b>Sorts</b> the lines. <code>-r</code> reversed, <code>-n</code> as numbers, <code>-u</code> without repeats, <code>-t , -k 3</code> by the 3rd field.</span></div>
    <div class="anat-row"><span>uniq</span><span>Reduces identical lines that come <b>one after another</b> to one. <code>-c</code> counts, <code>-d</code> the repeated ones, <code>-u</code> the ones seen once.</span></div>
    <div class="anat-row"><span>cut</span><span><b>Cuts a piece</b> out of each line: <code>-d , -f 2</code> the 2nd comma-separated field, <code>-c 1-10</code> the first 10 characters.</span></div>
    <div class="anat-row"><span>tr</span><span><b>Translates</b> or deletes characters: <code>tr a-z A-Z</code>, <code>-d</code> delete, <code>-s</code> squeeze repeats. Reads only from its input.</span></div>
  </div>
  <figcaption>All four tools work line by line and are joined to each other inside a pipeline.</figcaption>
</figure>

## sort: sorting

```text
~ $ sort names.txt
ada
alan
dennis
grace
katherine
linus
margaret
~ $ sort -r names.txt
margaret
linus
katherine
grace
dennis
alan
ada
```

`sort` prints the lines in alphabetical order, `-r` (*reverse*) turns it
around. It does not touch the file itself; to keep the result, `> other.txt`.

### Sorting numbers: `-n`

```text
~ $ cut -d , -f 3 data/sales.csv | tail -n +2 | sort
120
175
250
30
40
60
80
95
~ $ cut -d , -f 3 data/sales.csv | tail -n +2 | sort -n
30
40
60
80
95
120
175
250
```

The first sort looks wrong: `120` came before `30`. By default `sort` compares
as **text**: it looks at the first characters first, and `1` is smaller than
`3`. `-n` (*numeric*) looks at the **value** of the number at the start of the
line. (The `tail -n +2` in the middle dropped the header line; remember from
the Looking Inside Files section: "from line 2 to the end".)

### Sorting by a field: `-t` and `-k`

```text
~ $ cat data/sales.csv
name,city,amount
ada,London,120
alan,Manchester,80
grace,New York,250
linus,Helsinki,40
margaret,Boston,175
dennis,New York,60
katherine,Boston,95
ada,London,30
~ $ sort -t , -k 3 -n data/sales.csv
name,city,amount
ada,London,30
linus,Helsinki,40
dennis,New York,60
alan,Manchester,80
katherine,Boston,95
ada,London,120
margaret,Boston,175
grace,New York,250
~ $ sort -t , -k 3 -rn data/sales.csv | head -n 3
grace,New York,250
margaret,Boston,175
ada,London,120
```

- `-t ,` says which character separates the fields (a comma).
- `-k 3` means sort starting at the 3rd field.
- `-rn` reversed and numeric; then `head -n 3` gave the three biggest sales.

The header line `amount` is not a number, so `-n` counted it as 0 and put it on
top. Note: this terminal sorts capitals before lower case. On a real computer
the order can change with the language setting (*locale*); to get the same
order everywhere, you write `LC_ALL=C sort`.

## cut: cutting columns

```text
~ $ cut -d , -f 1 data/sales.csv | head -n 3
name
ada
alan
~ $ cut -d , -f 1,3 data/sales.csv | head -n 3
name,amount
ada,120
alan,80
~ $ cut -c 1-10 logs/app.log | head -n 2
2026-10-07
2026-10-07
~ $ cut -d ' ' -f 3- logs/app.log | head -n 3
INFO server started
INFO user ada logged in
WARN slow request /books
```

- `-d ,` is the delimiter, `-f 1` the 1st field.
- `-f 1,3` two fields; the delimiter is put between them again. `-f 2-4`
  would be a range.
- `-c 1-10` cuts **characters**, not fields: the date in the log is the first
  10 characters of every line.
- `-f 3-` from the 3rd field to the end of the line.

The delimiter of `cut` must be a single character. In the log file the delimiter is
a space; we write the space in quotes: `-d ' '`.

## uniq: repeats

```text
~ $ head -n 4 data/visits.log
10.0.0.1 /home
10.0.0.2 /books
10.0.0.1 /books
10.0.0.3 /home
~ $ cut -d ' ' -f 2 data/visits.log | uniq | wc -l
11
~ $ cut -d ' ' -f 2 data/visits.log | sort | uniq
/about
/books
/contact
/home
~ $ cut -d , -f 2 data/sales.csv | tail -n +2 | sort -u
Boston
Helsinki
London
Manchester
New York
```

`uniq` only joins identical lines that come **one after another**. In the
visit log `/home` appears on scattered lines, so `uniq` reduced 12 lines only
to 11. First `sort` brings the identical ones side by side, then `uniq` leaves
four pages. `sort -u` does both at once.

### Counting: `-c`, `-d`, `-u`

<figure class="fig">
  <div class="flow">
    <span class="node">cut -d ' ' -f 2<br><small>cut out the page</small></span><span class="arrow">→</span>
    <span class="node acc">sort<br><small>same ones side by side</small></span><span class="arrow">→</span>
    <span class="node acc">uniq -c<br><small>count</small></span><span class="arrow">→</span>
    <span class="node">sort -rn<br><small>most on top</small></span>
  </div>
  <figcaption>The pattern for the question "how many times each?". Because <code>uniq</code> only joins neighbouring lines, <code>sort</code> comes first.</figcaption>
</figure>

```text
~ $ cut -d ' ' -f 2 data/visits.log | sort | uniq -c
      2 /about
      4 /books
      1 /contact
      5 /home
~ $ cut -d ' ' -f 2 data/visits.log | sort | uniq -c | sort -rn
      5 /home
      4 /books
      2 /about
      1 /contact
~ $ cut -d ' ' -f 1 data/visits.log | sort | uniq -d
10.0.0.1
10.0.0.2
10.0.0.3
~ $ cut -d ' ' -f 1 data/visits.log | sort | uniq -u
10.0.0.4
10.0.0.5
10.0.0.6
10.0.0.7
```

- `uniq -c` writes in front of each line how many times it appeared.
- With `sort -rn` added, the most visited page came to the top. This chain is
  the pattern for the question "how many times each?"; the same for words,
  addresses, error types, anything.
- `uniq -d` prints the lines that appear more than once (once each), `uniq -u`
  only those that appear once: three addresses came back, four came once.

## tr: translating characters

```text
~ $ echo hello | tr a-z A-Z
HELLO
~ $ tr '[:lower:]' '[:upper:]' < poem.txt
ROSES ARE RED
VIOLETS ARE BLUE
THE SHELL IS FAST
AND SO ARE YOU
~ $ cat notes/messy.txt
Buy   milk  and   bread
Call    Ada
~ $ tr -s ' ' < notes/messy.txt
Buy milk and bread
Call Ada
~ $ echo 2026-10-07 | tr -d -
20261007
~ $ echo a,b,c | tr , '\n'
a
b
c
```

- `tr a-z A-Z` turns each letter of the first set into its partner in the
  second. `'[:lower:]' '[:upper:]'` is the same thing written with class names.
- `-s` (*squeeze*) reduces repeats of the same character to one: the
  scattered spaces were fixed.
- `-d` (*delete*) deletes: the dashes in the date are gone.
- `'\n'` is a line break: turning the commas into line breaks put each piece
  on its own line.

`tr` takes no file name; it always reads its input with `<` or from a pipe.

## All together: the most common words

```text
~ $ tr ' ' '\n' < poem.txt | sort | uniq -c | sort -rn | head -n 3
      3 are
      1 you
      1 so
```

Turn the spaces into line breaks (one word per line), sort, count, sort by the
count, take the first three. Five small commands, one line: `are` is the most
common word in the poem.

## Traps

```text
~ $ tr a-z A-Z poem.txt
tr: extra operand 'poem.txt'
Try 'tr --help' for more information.
~ $ sort -t , -k 2 data/sales.csv | head -n 2
margaret,Boston,175
katherine,Boston,95
~ $ sort -t , -k 2,2 data/sales.csv | head -n 2
katherine,Boston,95
margaret,Boston,175
```

- `tr a-z A-Z poem.txt`: `tr` takes the file name as an extra operand.
- `-k 2` looks from field 2 **to the end of the line**; the amounts decided the
  order of the two Boston lines: as text, `175` comes before `95`. `-k 2,2`
  looks only at field 2; on a tie the whole line is compared and `katherine`
  comes first.
- Using `uniq` without `sort` misses repeats.
- Do not sort a file into itself: `sort f > f` empties the file (remember the
  Redirection section).

## Summary

| Command | What it does |
|---|---|
| `sort` / `-r` / `-n` / `-u` | Sort / reversed / as numbers / without repeats |
| `sort -t , -k 3` | By the 3rd field |
| `uniq` / `-c` / `-d` / `-u` | Join neighbouring repeats / count / the repeated / the ones seen once |
| `cut -d , -f 2` | The 2nd field |
| `cut -c 1-10` | The first 10 characters |
| `tr a-z A-Z` | Translate letters |
| `tr -d x` / `tr -s ' '` | Delete / squeeze |

Learn the "how many times each?" pattern by heart: cut, `sort`, `uniq -c`,
`sort -rn`.
