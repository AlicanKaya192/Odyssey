`resume_matches` runs a 6-epoch training as 3 + 3 epochs, saving a checkpoint
in between and resuming; but the result is not the same as the uninterrupted
run (`False`), because Adam's state is not saved. Put the optimizer's
`state_dict()` into the checkpoint too and load it when resuming. The result
should be `True`.

**Expected output:**

```
True
```
