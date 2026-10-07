The books' `tags` field is a list. You will put it into a table in two
different ways.

**What to do:**

1. **One cell:** for every book, print the title and its tags joined with
   `|`. If it has no tags, the join stays empty.
2. **Separate rows:** for every book–tag pair, add the dictionary
   `{"book_id": ..., "tag": ...}` to the `pairs` list.
3. Using `pairs`, count in a `tag_counts` dictionary how many books each tag
   appears in. Print the tags in alphabetical order as `tag: count`.

**Expected output:**

```
Emma: classic|novel
Dune: scifi|classic
Ulysses:
Solaris: scifi
Persuasion: classic|romance|novel
pairs: 8
classic: 3
novel: 2
romance: 1
scifi: 2
```
