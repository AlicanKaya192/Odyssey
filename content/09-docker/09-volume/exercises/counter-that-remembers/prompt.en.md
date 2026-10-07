`counter.py` increases the counter by one every time it runs. But it writes
the counter to the working folder (`/app/count.txt`): every new container
starts from zero.

**What to do:** move the counter's file to the folder the volume is mounted
on: `/data/count.txt`.

Odyssey will run two separate containers, mounting `-v counter:/data` on
both.

**Expected outputs:**

```
count: 1
count: 2
```
