When the practice server sees the same name more than once it reads it as
"all of them". Ask for books tagged both `scifi` and `classic`, then compare
with the ones tagged only `scifi`.

**What to do:**

1. Ask for the two tags together by giving a **list** as the value of `tag`.
   Print the address that went out and the titles that came back.
2. Ask with `tag=scifi` alone and print how many books came back
   (`meta.total`).

**Expected output:**

```
http://api.odyssey.test/books?tag=scifi&tag=classic
Dune
scifi only: 8
```
