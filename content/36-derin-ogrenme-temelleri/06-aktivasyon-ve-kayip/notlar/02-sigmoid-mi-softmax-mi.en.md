Softmax makes the classes **compete**: when one grows, the others shrink,
and the total is always 1. That is right for tasks where each example has
exactly one class (this digit is either a 3 or an 8). In some tasks,
though, an example can have several labels: a photo can contain both a cat
and a dog. This is called **multi-label** classification, and a separate
sigmoid is used for each label:

```python
logits = torch.tensor([[2.0, -1.0, 0.5]])
print([round(v, 3) for v in torch.sigmoid(logits)[0].tolist()])
print([round(v, 3) for v in torch.softmax(logits, dim=1)[0].tolist()])
labels = torch.tensor([[1.0, 0.0, 1.0]])
print(round(nn.BCEWithLogitsLoss()(logits, labels).item(), 4))
```

```text
[0.881, 0.269, 0.622]
[0.786, 0.039, 0.175]
0.3048
```

- Sigmoid judges each label on its own: the first and third labels are
  above 0.5, both "present". They do not sum to 1.
- Softmax makes the same scores compete; the third label is higher than the
  second but has to share with the first.
- The loss for a multi-label task is `BCEWithLogitsLoss`; the target is a row
  of 0s and 1s.

<figure class="fig">
  <div class="versus">
    <div><h5>Single label (multi-class)</h5>The last layer has one logit per class, the loss is <code>CrossEntropyLoss</code>, the target is a class number.</div>
    <div><h5>Several labels (multi-label)</h5>The last layer has one logit per label, the loss is <code>BCEWithLogitsLoss</code>, the target is a row of 0/1.</div>
  </div>
  <figcaption>Two different tasks, two different losses.</figcaption>
</figure>
