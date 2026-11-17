Putting a softmax in the model's last layer and giving its output to
`CrossEntropyLoss` raises no error; why it is bad shows in the loss itself.
Imagine a **perfect** model, very sure of the right class:

```python
perfect = torch.tensor([[10.0, 0.0, 0.0]])
target = torch.tensor([0])
loss_fn = nn.CrossEntropyLoss()
print(round(loss_fn(perfect, target).item(), 4))
print(round(loss_fn(torch.softmax(perfect, dim=1), target).item(), 4))
print(round(loss_fn(torch.tensor([[1.0, 0.0, 0.0]]), target).item(), 4))
```

```text
0.0001
0.5515
0.5514
```

- Given logits, the perfect model's loss is almost 0.
- Given probabilities, the loss cannot go below 0.55: the loss
  function takes the probabilities for logits and applies softmax a second
  time. "Logits" squeezed between 0 and 1 can differ by at most 1; the third
  line shows that the loss of `[1, 0, 0]` is almost the same.
- The result: however much the model improves, the loss barely changes, the
  gradients stay small and learning slows down.

The symptom: if the training loss refuses to go below a certain value,
check whether there is a softmax in the last layer.
