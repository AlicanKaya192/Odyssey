Every filtering option is optional. The ones not given must not appear in the
address at all.

**What to do:**

1. Write the function `search(author, tag, sort)`. Any of the three values
   may be `None`. Build the `params` dictionary from the three (requests
   already leaves out the `None` ones), add 20 as `per_page`, and return the
   **list of titles**.
2. Run the three searches below. If the list is empty print
   `nothing found`, otherwise print the titles joined with a comma and a
   space.

**Expected output:**

```
Mrs Dalloway, To the Lighthouse, Orlando
A Wizard of Earthsea
Fiasco, The Cyberiad, Solaris
nothing found
```
