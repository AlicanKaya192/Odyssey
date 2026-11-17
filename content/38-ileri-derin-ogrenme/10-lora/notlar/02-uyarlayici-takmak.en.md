With the adaptation plugged in the model does well on the new task, but no
longer on the old one: in the lesson, if we look at the old task's data after
fine-tuning, the accuracy drops. This is where LoRA really pays off: the base
is stored once, for every task only the small `A` and `B` are stored and
plugged in when needed. The code below uses the trained `net` from the
lesson.

```python
print(accuracy(net, xa, ya) < 0.6)
state = net.state_dict()
adapter = {k: state[k].clone() for k in ("0.A", "0.B")}
print(sorted(adapter), sum(v.numel() for v in adapter.values()))
fresh = nn.Sequential(LoRALinear(net[0].base, r=2), *net[1:])
print(accuracy(fresh, xb, yb) > 0.8)
result = fresh.load_state_dict(adapter, strict=False)
print(accuracy(fresh, xb, yb) > 0.8, len(result.missing_keys))
```

```text
True
['0.A', '0.B'] 140
False
True 6
```

- The first line: with the adaptation plugged in, the accuracy on the old
  task is below 0.6.
- The adapter is just two tensors, 140 values. Instead of storing the whole
  base model again for every task, storing this much is enough.
- `fresh`: a **new** LoRA layer on top of the same base; since `B` is zero it
  behaves like the base and fails on the new task.
- `load_state_dict(..., strict=False)` loads only the given keys and leaves
  the others alone; the 6 missing keys (the base weights) are expected.
  With `strict=True` (the default) it would raise an error because of the
  missing keys.
- Once the adapter was loaded, the success on the new task came back.

So next to a single base model, separate adapters can be kept for dozens of
tasks; whichever task a request belongs to, its `A` and `B` are plugged in.
Since the base is frozen, the adapters do not damage each other.
