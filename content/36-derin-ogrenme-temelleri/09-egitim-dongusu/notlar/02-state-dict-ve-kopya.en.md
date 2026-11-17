`model.state_dict()` is a dictionary that gives all the model's parameters
with their names. But the tensors inside it are **not copies of the
parameters; they are the parameters themselves**:

```python
saved = model.state_dict()
copied = copy.deepcopy(model.state_dict())
with torch.no_grad():
    model[0].bias.add_(1.0)
print(torch.equal(saved["0.bias"], model[0].bias))
print(torch.equal(copied["0.bias"], model[0].bias))
print(list(copied.keys()))
```

```text
True
False
['0.weight', '0.bias', '2.weight', '2.bias']
```

- `saved` changed together with the model: when the bias went up by 1, the
  value in the dictionary went up too. Had we kept this as the "best state"
  in the loop, at the end of training we would have the **last** state, not
  the best.
- `copy.deepcopy` takes a real copy of the tensors; the copy does not change
  when the model does.
- The keys are the layers' names: the position number in `nn.Sequential`
  (`0.weight`), the attribute name in your own class (`hidden.weight`). In
  the Saving section we write the same dictionary to disk.
