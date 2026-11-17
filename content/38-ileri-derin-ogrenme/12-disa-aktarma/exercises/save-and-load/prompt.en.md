Save the exported `ep` to the file `model.pt2` with `torch.export.save`, load
it back with `torch.export.load` and make it callable with `.module()`. The
last line prints the shape and whether it gives the same result as the
original model.

**Expected output:**

```
torch.Size([4, 2]) True
```
