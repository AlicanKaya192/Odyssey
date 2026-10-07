Collect the books tagged classic in pages of 4; do not compute page numbers,
follow the `next` link the server gives.

**What to do:**

1. The first address: `BASE + "/books?tag=classic&per_page=4"`.
2. In a `while url:` loop, request it and add `data` to a `classics` list;
   if there is a `links.next`, `url = BASE + next`, otherwise `None`.
3. Print each `next` address followed, then how many pages you went
   through and how many books you collected.

**Expected output:**

```
next: /books?tag=classic&per_page=4&page=2
next: /books?tag=classic&per_page=4&page=3
pages: 3
classics: 12
```

Notice that the `tag` and `per_page` parameters are kept in the `next`
address.
