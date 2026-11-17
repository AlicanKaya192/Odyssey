If we do not want a layer to learn, we switch off `requires_grad` on its
parameters. This is called **freezing**; in transfer learning in the
Computer Vision module, pretrained layers are protected this way.

```python
for p in model.hidden.parameters():
    p.requires_grad = False
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(trainable, total)
before_w = model.hidden.weight.clone()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
loss = nn.CrossEntropyLoss()(model(x), y)
loss.backward()
optimizer.step()
print(torch.equal(before_w, model.hidden.weight), model.hidden.weight.grad)
```

```text
51 163
True None
```

- The 112 parameters of the `hidden` layer were frozen; only the 51
  parameters of the `out` layer will be trained.
- No gradient was computed for the frozen layer (`None`) and `step()` did
  not change it.
- Giving the optimizer all the parameters is harmless: it skips parameters
  that have no gradient. You can also give it only the trainable ones:
  `[p for p in model.parameters() if p.requires_grad]`.
