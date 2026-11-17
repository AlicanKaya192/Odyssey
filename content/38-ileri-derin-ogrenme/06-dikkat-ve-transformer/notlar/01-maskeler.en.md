PyTorch accepts two kinds of masks: **boolean** (`True` = do not look) and
**numeric** (`−∞` where not to look, 0 elsewhere; added to the scores).
`nn.Transformer.generate_square_subsequent_mask` gives the numeric causal
mask ready-made. Both give the same result:

```python
import torch
from torch import nn

float_mask = nn.Transformer.generate_square_subsequent_mask(4)
bool_mask = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)
print(float_mask[1].tolist())
torch.manual_seed(0)
attn = nn.MultiheadAttention(8, 2, batch_first=True)
x = torch.randn(2, 4, 8)
a, _ = attn(x, x, x, attn_mask=float_mask)
b, _ = attn(x, x, x, attn_mask=bool_mask)
print(torch.allclose(a, b))

everything = torch.tensor([[False, False, False, False], [True, True, True, True]])
out, _ = attn(x, x, x, key_padding_mask=everything)
print(torch.isnan(out[0]).any().item(), torch.isnan(out[1]).any().item())
```

```text
[0.0, 0.0, -inf, -inf]
True
False True
```

- Row 1 of the numeric mask is `[0, 0, −∞, −∞]`: position 1 sees the first
  two.
- The last line shows a trap: when **all** keys of the second sequence are
  masked, only `−∞` goes into the softmax, the result is `0 / 0` and the
  output becomes `nan`. Examples of length 0 must be removed from the data.

## Common mistakes

| Mistake | Result |
|---|---|
| Writing `key_padding_mask=(ids != 0)` | An inverted mask: the model looks only at padding, no error |
| Giving the mask as `(T, B)` instead of `(B, T)` | A shape error, or the mask applied to the wrong sequences |
| Forgetting the causal mask in a language model | Very good training loss, very bad generation: the model saw the answer |
| Masking every position | `nan` output, `nan` loss |

The third mistake is the sneakiest: in training the model looks at the word
on the right and copies it, the loss goes towards zero; in generation there
is no word on the right, so it cannot produce anything.
