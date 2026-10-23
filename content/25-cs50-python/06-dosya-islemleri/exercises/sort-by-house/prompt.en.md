The first line of `students.csv` is a header: `name,house`. Read the file with `csv.DictReader` and print the students **sorted by house**, as `Harry is in Gryffindor`. Use `key=lambda ...` for the sort. Students in the same house keep their order from the file (`sorted` does not reorder ties).

Example run (the prompt can say anything you like; only your output and your file are checked):

```text
$ python cozum.py
Hermione is in Gryffindor
Harry is in Gryffindor
Cedric is in Hufflepuff
Luna is in Ravenclaw
Draco is in Slytherin
```
