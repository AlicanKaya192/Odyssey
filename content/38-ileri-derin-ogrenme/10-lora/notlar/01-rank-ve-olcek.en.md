LoRA has two settings: the rank `r` and the scale `alpha`. The numbers show
why it is so popular for large models. For a 4096 × 4096 layer, common in a
language model:

```python
import torch

for r in [1, 4, 16, 64]:
    lora = r * (4096 + 4096)
    print(r, lora, round(100 * lora / (4096 * 4096), 2))
```

```text
1 8192 0.05
4 32768 0.2
16 131072 0.78
64 524288 3.12
```

- The layer itself has 16,777,216 values. A rank-16 LoRA stays below one per
  cent (column: percentage of the full layer).
- As the rank grows the adaptation can learn more but needs more memory and
  data. For most jobs 4–16 is enough; the best is chosen with validation.

The rank of the product `B · A` is at most `r`; however long it is trained,
the adaptation weight cannot exceed that limit:

```python
gen = torch.Generator().manual_seed(0)
B = torch.randn(64, 4, generator=gen)
A = torch.randn(4, 64, generator=gen)
print((B @ A).shape, torch.linalg.matrix_rank(B @ A).item())
```

```text
torch.Size([64, 64]) 4
```

A 64 × 64 matrix, but its rank is 4. This is LoRA's assumption too: the
change made by fine-tuning gathers in a small number of "directions".

## The scale: alpha / r

In the lesson the adaptation's contribution was multiplied by `alpha / r`.
The reason is to stop the size of the adaptation from changing by itself when
the rank changes: with `alpha` fixed, doubling the rank halves each
component's share, and the learning rate need not be retuned. Common choices
are `alpha = 2 · r` or a fixed `alpha` that does not change with the rank.

## Where does LoRA go?

In the lesson we put it on a single layer. In Transformers the most common
place is the attention layer's query and value projections (the `q` and `v`
linear layers); putting it on more layers means more flexibility but more
parameters. The rule is the same: think about which layers need to change,
then wrap only those.
