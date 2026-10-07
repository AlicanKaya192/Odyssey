`main.py` uses a function from a folder (a package) called `textkit`:
`from textkit.shout import shout`. For this to work, the image must contain
`/app/textkit/shout.py`; the folder must be kept.

**What to do:** in place of the comment line, write the `COPY` line that
copies the `textkit` folder **as a folder** into `/app/textkit/`.

If you write `COPY textkit/ .`, the folder's contents are poured straight
into `/app` and the `import` fails.

**Expected output:**

```
FOLDERS MATTER!
```
