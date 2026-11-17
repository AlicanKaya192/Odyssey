The lesson's loop kept the two losses of each epoch in `history`. Let us
look at a few epochs:

```python
for epoch in [1, 5, 10, 20, 30]:
    train_loss, val_loss = history[epoch - 1]
    print(epoch, round(train_loss, 3), round(val_loss, 3))
```

```text
1 0.696 0.431
5 0.228 0.353
10 0.212 0.359
20 0.206 0.409
30 0.178 0.432
```

In the first epochs both losses fall together. Then the training loss keeps
falling while the validation loss rises: the gap between them widens. How to
read the two curves together:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Both falling</span><span>The model is learning; keep training.</span></div>
    <div class="anat-row"><span>Training falls, validation rises</span><span>Overfitting: the model is memorising the training data. Stop at the best epoch, add regularisation.</span></div>
    <div class="anat-row"><span>Both high and flat</span><span>Underfitting: the model is too small, the learning rate is off or there are too few epochs.</span></div>
    <div class="anat-row"><span>The loss jumps, becomes <code>nan</code></span><span>The learning rate is too high.</span></div>
  </div>
  <figcaption>Reading the training and validation losses together.</figcaption>
</figure>

A single loss number says none of this; you need to see the two curves side
by side. That is why keeping the losses in a list and plotting them later
(or printing a few epochs) should be a habit.
