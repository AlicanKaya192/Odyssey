`DownBlock` is a residual block that raises the channel count and halves the
map. The main path is ready; write `self.shortcut`: an `nn.Sequential` that
brings `x` to the same shape as the main path's output:
`Conv2d(in_ch, out_ch, kernel_size=1, stride=2, bias=False)` and
`BatchNorm2d(out_ch)`.

**Expected output:**

```
(2, 32, 4, 4)
576
```
