The most intuitive explanation method, which needs no gradients, is
**occlusion sensitivity**: cover a region of the picture with zeros and see
how much the probability of the right class drops. Slide the region over the
picture; the region that lowers the probability most is where the model
trusts most. This note uses the trained model from the lesson.

```python
def occlusion_map(image, target, patch=6):
    steps = image.shape[-1] // patch
    drops = torch.zeros(steps, steps)
    with torch.no_grad():
        base = F.softmax(model(image[None]), dim=1)[0, target]
        for row in range(steps):
            for col in range(steps):
                r0, c0 = row * patch, col * patch
                covered = image.clone()
                covered[:, r0:r0 + patch, c0:c0 + patch] = 0
                prob = F.softmax(model(covered[None]), dim=1)[0, target]
                drops[row, col] = base - prob
    return drops


drops = occlusion_map(x_test[2], y_test[2].item())
row, col = divmod(drops.argmax().item(), 4)
print(SHAPES[y_test[2]], drops.shape, (row, col), (row * 6, col * 6))
print((drops > 0.5).sum().item())
```

```text
square torch.Size([4, 4]) (1, 2) (6, 12)
1
```

- The 24 × 24 picture was split into 16 patches of 6 × 6; each patch was
  covered once.
- The picture is a square (the third line in the lesson: its box spans x
  9–17, y 2–11). The largest drop is at patch (1, 2): rows 6–11 and columns
  12–17 of the picture, the square's lower right corner. It is the only patch
  that lowers the probability by more than half.
- The cost: one forward pass per patch (16 here). On a big picture with small
  patches it takes thousands of passes; Grad-CAM makes do with one forward
  and one backward pass.
- It may not work on every picture: if the model is very confident and the
  shape spreads over several patches, covering a single patch does not move
  the probability at all (in the lesson's second picture, the circle, no
  patch lowers the probability even by 0.01).
- The value used for covering (0, grey, blurred) can change the result: a
  black patch may also look like "a new shape" to the model.
