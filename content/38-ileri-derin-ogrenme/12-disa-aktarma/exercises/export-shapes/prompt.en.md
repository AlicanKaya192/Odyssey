`export_shapes(batches)` exports the ready model with a 4-row example input,
calls it with every given batch size and returns the output shapes. As it is,
it fails for sizes other than 4: free the batch size (dimension 0) with
`torch.export.Dim` and `dynamic_shapes`.

**Expected output:**

```
[[3, 2], [7, 2]]
```
