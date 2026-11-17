`load_state_dict` matches the keys in the file against the model's keys one
by one. If the model has changed (a layer was added, a layer got wider), it
raises an error that says which key did not fit and why:

```python
saved = torch.load("model.pt", weights_only=True)
deeper = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 8),
                       nn.ReLU(), nn.Linear(8, 3))
try:
    deeper.load_state_dict(saved)
except RuntimeError as error:
    for line in str(error).splitlines()[1:]:
        print(line.strip().split(":")[0])

longer = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3),
                       nn.ReLU(), nn.Linear(3, 3))
result = longer.load_state_dict(saved, strict=False)
print(result.missing_keys)
```

```text
Missing key(s) in state_dict
size mismatch for 2.weight
size mismatch for 2.bias
['4.weight', '4.bias']
```

- In the deeper model, `4.weight` and `4.bias` are not in the file
  (**missing**); `2.weight` is `(3, 8)` in the file and `(8, 8)` in the model
  (**size mismatch**).
- `strict=False` **reports** missing and unexpected keys instead of raising,
  and loads the ones that exist. It helps when adding a new output layer on
  top of a pretrained body (transfer learning in the advanced module).
- `strict=False` does not forgive a shape mismatch; that is still an error.
- To open a file saved on a GPU on a computer without one:
  `torch.load(path, map_location="cpu", weights_only=True)`.
