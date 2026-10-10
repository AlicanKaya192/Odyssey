`Registry` keeps added objects in a set; even if the objects are deleted
elsewhere in the program, they live on in the registry. Replace the set with
`weakref.WeakSet`: a deleted object must drop out of the registry by itself.
(Note the `del item` line at the bottom: after the loop ends, the name `item`
keeps pointing to the last object; that is a reference too.) The expected
output:

```
3
2
0
```

**Expected output:**

```
3
2
0
```
