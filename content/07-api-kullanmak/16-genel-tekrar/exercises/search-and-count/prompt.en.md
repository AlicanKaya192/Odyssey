A review of Sections 01, 06 and 07: a search with parameters, the address that
went out and the result.

**What to do:**

1. Ask `/books` for **science fiction** books published in **1960 or
   later**, sorted by year **oldest first**, with a page size of 20. Give
   them all with `params=`.
2. Print the address that went out, the total count and each book as
   `year title`.

**Expected output:**

```
http://api.odyssey.test/books?tag=scifi&year_min=1960&sort=year&per_page=20
total: 8
1961 Solaris
1965 Dune
1965 The Cyberiad
1969 Dune Messiah
1969 The Left Hand of Darkness
1971 The Lathe of Heaven
1974 The Dispossessed
1986 Fiasco
```
