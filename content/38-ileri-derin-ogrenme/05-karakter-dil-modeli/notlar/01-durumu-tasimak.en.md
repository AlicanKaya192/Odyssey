While generating we carried the LSTM's state instead of re-reading the whole
text at every step. Let us see that the two give the same result: the code
below uses the lesson's trained model; it reads "the cat sat" once in one
piece and once character by character after the first 5 characters.

```python
model.eval()
with torch.no_grad():
    ids = torch.tensor([[index[c] for c in "the cat sat"]])
    full, _ = model(ids)
    logits, state = model(ids[:, :5])
    for t in range(5, ids.shape[1]):
        logits, state = model(ids[:, t:t + 1], state)
print(ids.shape[1], torch.allclose(full[0, -1], logits[0, -1], atol=1e-5))
```

```text
11 True
```

The logits of the last character are the same on both roads. The LSTM's
whole past lives in the `(h, c)` state; giving the state is giving the past
again.

## State in training: truncated backpropagation

In a very long text (a book) the windows follow one another, and carrying
the state from one window to the next lets the network see a longer past.
But walking the derivative back through the whole book is impossible in
memory and time. The fix is **truncated backpropagation through time**
(truncated BPTT):

```text
state = None
for x, y in windows_in_order:
    logits, state = model(x, state)
    state = tuple(s.detach() for s in state)
    ...  # loss, backward, step
```

`detach()` carries the **value** of the state to the next window but cuts the
derivative link: the derivative walks back only inside that window. Forget
`detach` and the second window's `backward()` tries to reach the first
window's computation graph, which has already been freed, and fails with
"Trying to backward through the graph a second time".
