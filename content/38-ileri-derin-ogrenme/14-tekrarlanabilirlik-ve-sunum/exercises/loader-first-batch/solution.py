import torch


def first_batch(seed):
    data = torch.utils.data.TensorDataset(torch.arange(10))
    gen = torch.Generator().manual_seed(seed)
    loader = torch.utils.data.DataLoader(data, batch_size=4, shuffle=True, generator=gen)
    return next(iter(loader))[0].tolist()

print(first_batch(0) == first_batch(0))
print(len(first_batch(1)))
