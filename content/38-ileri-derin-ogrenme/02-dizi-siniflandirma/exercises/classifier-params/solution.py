from torch import nn


def classifier_params(vocab, dim, hidden):
    layers = [nn.Embedding(vocab, dim), nn.LSTM(dim, hidden, batch_first=True),
              nn.Linear(hidden, 2)]
    return sum(p.numel() for layer in layers for p in layer.parameters())

print(classifier_params(10, 8, 16))
print(classifier_params(100, 4, 4))
