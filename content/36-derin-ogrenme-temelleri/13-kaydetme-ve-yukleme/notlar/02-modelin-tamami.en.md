`torch.save(model)` saves not only the numbers but **the model object
itself**. It looks like a shortcut, but it has two problems:

```python
torch.save(model, "whole.pt")
try:
    torch.load("whole.pt", weights_only=True)
except Exception as error:
    print(type(error).__name__, str(error).split(".")[0])
loaded = torch.load("whole.pt", weights_only=False)
print(type(loaded).__name__, torch.equal(loaded(x), model(x)))
```

```text
UnpicklingError Weights only load failed
Sequential True
```

- It was refused in the safe mode: the file holds `Sequential` and `Linear`
  objects. It could only be opened in the unsafe mode
  (`weights_only=False`); we wrote this file ourselves, so that is fine here,
  but not for someone else's.
- The file is tied to the model's class **by name**. If you save a class you
  wrote yourself (`class TableNet(nn.Module)`) this way, the loading program
  must have a class with the same name in the same module; move the code or
  rename the class and the file no longer opens.
- A state_dict avoids both problems: only tensors, it opens in the safe mode,
  and you can edit the class as you like.
