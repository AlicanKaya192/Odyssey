In a plain RNN the hidden state is recomputed at every step: old information
is multiplied by `W_h` and passed through `tanh`. An **LSTM** (long
short-term memory; Hochreiter and Schmidhuber, 1997) adds a separate **cell
state** next to it and updates it not by multiplying but by **adding**:

$$c_t = f_t \cdot c_{t-1} + i_t \cdot g_t$$

- `f` (the forget gate) says how much of the old stays,
- `i` (the input gate) says how much of the new information (`g`) is written,
- a third gate `o` (output) says how much of the cell goes out to the hidden
  state. Gates are between 0 and 1, computed with a sigmoid, and learned by
  the network itself.

Let us see in numbers what happens when the gates are fixed:

```python
def lstm_cell(c, forget, write, new):
    return forget * c + write * new


c = 1.0
for step in range(50):
    c = lstm_cell(c, forget=0.99, write=0.0, new=0.0)
h = 1.0
for step in range(50):
    h = 0.9 * h
print(round(h, 4), round(c, 4))
c = lstm_cell(c, forget=0.0, write=1.0, new=-1.0)
print(c)
```

```text
0.0052 0.605
-1.0
```

- Information multiplied by 0.9 at each step falls to 0.0052 in 50 steps; a
  cell whose forget gate stays open at 0.99 keeps 0.605 of it. The
  derivative going back through the cell passes the same factors (the `f`
  values), so it does not vanish.
- When the forget gate is 0 and the input gate 1, the cell wipes out the old
  completely and writes the new value. The model learns what to forget and
  when: like erasing the old subject when a new sentence's subject arrives.
- A **GRU** (gated recurrent unit, 2014) is a simplified version of the same
  idea: two gates, no separate cell state. On most tasks it comes close to an
  LSTM with fewer parameters.
- Until the mid-2010s the LSTM was standard in machine translation and
  speech recognition. Today large language models are built with the
  attention mechanism; the reason is in the next two sections.
