Chains that are written again and again in real work. Replace the file names
with your own files.

## How many times each?

```bash
cut -d ' ' -f 2 visits.log | sort | uniq -c | sort -rn
```

Cut, sort, count, sort by the count. For the top five, add `| head -n 5` at
the end.

## The most common words

```bash
tr ' ' '\n' < text.txt | sort | uniq -c | sort -rn | head -n 10
```

If upper and lower case should count as the same, add `tr A-Z a-z` at the
start.

## The distinct values of a column

```bash
tail -n +2 sales.csv | cut -d , -f 2 | sort -u
```

`tail -n +2` drops the header line.

## The N biggest lines

```bash
sort -t , -k 3 -rn sales.csv | head -n 3
```

## Error types

```bash
grep -i error app.log | cut -d ' ' -f 4- | sort | uniq -c
```

Filter first, then cut out the text of the error and count.

## Repeated lines

```bash
sort names.txt | uniq -d
```

Finds the ones written twice in a list.

## Fix scattered spaces

```bash
tr -s ' ' < messy.txt > clean.txt
```

Always write the result to a **different** file; `> messy.txt` empties the file
before it is read.
