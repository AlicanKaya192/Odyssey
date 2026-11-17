The starter builds an LSTM and an input padded with zeros at the end.
`compare_final_states(lengths)` should return two lists:

- with the LSTM run on the input **without packing**, is each sequence's
  last state (`h[0, i]`) the same as the output of its last real step
  (`out[i, n - 1]`) by `torch.allclose`;
- the same question for the last state of the run packed with
  `pack_padded_sequence(..., enforce_sorted=False)`.

**Expected output:**

```
[[True, True, False], [True, True, True]]
[[True, False], [True, True]]
```
