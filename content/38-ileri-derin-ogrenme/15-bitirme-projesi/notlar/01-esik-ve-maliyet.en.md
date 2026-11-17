In the lesson we used `argmax`: a fault if the fault probability passes 0.5.
But the two kinds of error do not cost the same. Missing a fault (a false
negative) leads to the machine breaking; a needless alarm (a false positive)
to a technician looking for nothing. If the costs differ, the threshold need
not be 0.5 either: **the threshold with the smallest cost** is chosen.

Below are hand-written fault probabilities and true labels for ten windows; a
missed fault costs 10, a needless alarm 1:

```python
import torch

probs = torch.tensor([0.05, 0.1, 0.2, 0.35, 0.4, 0.55, 0.6, 0.8, 0.9, 0.95])
labels = torch.tensor([0, 0, 0, 1, 0, 0, 1, 1, 1, 1])


def costs(threshold, fn_cost=10, fp_cost=1):
    pred = (probs >= threshold).long()
    fn = ((pred == 0) & (labels == 1)).sum().item()
    fp = ((pred == 1) & (labels == 0)).sum().item()
    return fn, fp, fn * fn_cost + fp * fp_cost


for t in [0.5, 0.3]:
    print(t, costs(t))
print(min([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], key=lambda t: costs(t)[2]))
```

```text
0.5 (1, 1, 11)
0.3 (0, 2, 2)
0.3
```

- Threshold 0.5: one fault was missed (the one with probability 0.35), and
  there is one needless alarm; cost 11.
- Threshold 0.3: no fault missed, two needless alarms; cost 2. More alarms
  but much cheaper.
- Among the candidate thresholds the cheapest is 0.3.

As the threshold falls, recall rises or stays the same and precision usually
falls: the two pull against each other. In a real project this computation
is done with the model's probabilities on the **validation** data
(`torch.softmax(model(x[val]), dim=1)[:, 1]`), the chosen threshold is written
into the delivery package's description and measured once on the test set.
The costs are an engineering decision; they come from the job itself, not
from the model.
