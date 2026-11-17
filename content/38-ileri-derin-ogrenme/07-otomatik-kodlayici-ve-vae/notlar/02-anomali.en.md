An autoencoder rebuilds well only the **kind** of data it has seen. That is
not a weakness but a tool: an example with a large reconstruction error is
"out of the ordinary". Unlabelled **anomaly detection** works this way. The
code below uses the lesson's trained `ae`; it compares the test digits with
random noise images.

```python
def errors(model, data):
    with torch.no_grad():
        return ((model(data) - data) ** 2).mean(dim=1)


noise = torch.rand(100, 64, generator=torch.Generator().manual_seed(2))
train_err = errors(ae, x_train)
limit = torch.quantile(train_err, 0.99)
print(errors(ae, noise).mean().item() > errors(ae, x_test).mean().item())
print((errors(ae, noise) > limit).float().mean().item() > 0.9)
```

```text
True
True
```

- The noise's mean error is larger than the digits'.
- The threshold is the 99th percentile of the training errors
  (`torch.quantile`): only 1% of the training digits are above it. More than
  90% of the noise images cross the threshold, so they are flagged as
  "anomalies".

The sensor fault detector in this module's capstone works with labelled
data. In reality fault examples are often rare or missing; then training an
autoencoder on healthy recordings only and putting a threshold on the
reconstruction error is a common start. The threshold is chosen with
validation data and the cost of a false alarm.
