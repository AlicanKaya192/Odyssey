This workflow has **three** mistakes:

- Because of two of them, GitHub does not run the file at all.
- Because of the third, the `pip install` step cannot find the `requirements.txt` file.

Fix all of them. The job should run on `ubuntu-latest`. When you press Run, the check reports the first mistake it finds; you can fix one and run again.
