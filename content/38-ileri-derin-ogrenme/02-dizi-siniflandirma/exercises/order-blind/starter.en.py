import torch
from torch import nn


class SeqClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8, hidden=16):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.lstm = nn.LSTM(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        out, (h, c) = self.lstm(self.emb(x))
        return self.head(h[-1])


class BagClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.head = nn.Linear(dim, 2)

    def forward(self, x):
        return self.head(self.emb(x).mean(dim=1))


def order_blind(seqs):
    torch.manual_seed(0)
    bag, lstm = BagClassifier(), SeqClassifier()
    x = torch.tensor(seqs)
    # Write your code here
    return []

print(order_blind([[1, 2, 3, 4], [5, 5, 0, 9]]))
