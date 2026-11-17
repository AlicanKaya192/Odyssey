The pictures are written to a temporary folder. Build `data` as an
`ImageFolder` that gives one channel in [0, 1] (`v2.ToImage`, `v2.Grayscale`,
`v2.ToDtype`), and make `loader` a `DataLoader` with batch 8 that shuffles
with `generator=torch.Generator().manual_seed(0)`.

**Expected output:**

```
40 5
(8, 1, 16, 16) torch.int64
True
```
