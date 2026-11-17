In a real project (for example telling cats from dogs with a ResNet trained on
ImageNet) the steps are the same as in the lesson; only the body is bigger.
Here we write `weights=None` to avoid downloading weights; in a real project
you write `weights=models.ResNet18_Weights.DEFAULT` and the weight file is
downloaded from the internet on first use.

```python
from torch import nn
from torchvision import models

model = models.resnet18(weights=None)
for p in model.parameters():
    p.requires_grad = False
model.fc = nn.Linear(model.fc.in_features, 2)
trainable = [name for name, p in model.named_parameters() if p.requires_grad]
print(trainable)
print(sum(p.numel() for p in model.parameters() if p.requires_grad))
```

```text
['fc.weight', 'fc.bias']
1026
```

- First all parameters are frozen, **then** the new `fc` is attached: a new
  layer's parameters are trainable by default.
- Of more than 11 million parameters only 1,026 are trained (512 × 2 + 2). A
  few hundred pictures are enough for that.

Checklist:

1. Prepare the pictures as the model expects: `weights.transforms()` (size,
   crop, ImageNet mean and deviation). Turn grey pictures into RGB.
2. Freeze the body, attach a new head; give the optimizer only the head's
   parameters.
3. While training, keep the body in `eval()` after `model.train()`
   (BatchNorm).
4. When validation accuracy stalls, you can unfreeze the body's last stage
   (`layer4`) and fine-tune with a small learning rate.
5. When predicting, `model.eval()` and `torch.no_grad()`.
