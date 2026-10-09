Write the function `write_people(path, people)`: write the list of
dictionaries `people` to the file with `csv.DictWriter`; the columns are the
first dictionary's keys (`list(people[0])`), the header line first. Then read
the file back and return its lines as a list (`read().splitlines()`).

**Expected output:**

```
name,city
Ada,"London, UK"
Alan,Wilmslow
```
