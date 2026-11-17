## Sequences

| Written | What |
|---|---|
| `nn.Embedding(V, D, padding_idx=0)` | id → vector, the padding id's vector is zero |
| `nn.LSTM(D, H, batch_first=True)` | input `(B, T, D)`; output and `(h, c)` |
| `pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)` | skipping the padding |
| `nn.Conv1d(C, K, kernel_size, dilation=d)` | input `(B, C, T)`; dilated convolution |
| `x.transpose(1, 2)` | `(B, T, D)` → `(B, D, T)` |
| `torch.triu(torch.ones(T, T, dtype=torch.bool), 1)` | causal mask (the future is `True`) |
| `nn.TransformerEncoder(layer, num_layers)` | stacking encoder blocks |

## Generative models

| Written | What |
|---|---|
| `F.mse_loss(model(x), x)` | the autoencoder's loss |
| `mu + torch.exp(0.5 * logvar) * torch.randn_like(mu)` | reparameterisation |
| `-0.5 * torch.mean(torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1))` | the KL term |
| `loss_fn(D(real), ones) + loss_fn(D(fake.detach()), zeros)` | the discriminator's loss |
| `loss_fn(D(fake), ones)` | the generator's loss |

## Few labels

| Written | What |
|---|---|
| `F.normalize(z, dim=1)`; `z @ z.T / tau` | cosine similarity / temperature |
| `sim.fill_diagonal_(float("-inf"))` | removing self-similarity from the candidates |
| `F.cross_entropy(sim, target)` | NT-Xent |
| `base.requires_grad_(False)` | freezing |
| `x @ A.T @ B.T * (alpha / r)` | LoRA's contribution |
| `W + (alpha / r) * B @ A` | folding the adaptation into the weight |

## Deployment

| Written | What |
|---|---|
| `time.perf_counter()`, the shortest | measuring time |
| `torch.inference_mode()` | prediction: no graph |
| `torch.autocast("cpu", dtype=torch.bfloat16)` | mixed precision |
| `record_function("name")` + `profile(...)` | profiling |
| `torch.export.export(m, (x,), dynamic_shapes=({0: Dim("batch")},))` | exporting |
| `torch.export.save` / `torch.export.load(...).module()` | save / load a `.pt2` |
| `torch.cond(condition, f, g, (x,))` | exportable branching |
| `torch.round(w / scale).clamp(-127, 127).to(torch.int8)` | `int8` quantisation |
| `prune.l1_unstructured(m, "weight", amount=0.5)` | pruning |
| `random.seed`, `np.random.seed`, `torch.manual_seed` | seeds |
| `DataLoader(..., generator=torch.Generator().manual_seed(s))` | seeded shuffling |
| `torch.use_deterministic_algorithms(True)` | deterministic operations |

## Measuring

| Situation | Measure |
|---|---|
| Balanced classes | accuracy |
| A minority class (fault, anomaly) | precision, recall; threshold by cost |
| Forecasting (a number) | MAE; against a baseline |
| A generative model | the generated examples themselves (e.g. cluster shares) |
| Learning without labels | nearest-neighbour accuracy, a linear probe |
| A shrunk model | the accuracy gap to the original |
| An exported model | a golden output (`allclose`) |
