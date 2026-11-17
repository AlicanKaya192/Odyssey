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
from torch.utils.data import TensorDataset, DataLoader
from dl_data import make_sequences

x, y = make_sequences(600, length=12, seed=3)
x, y = torch.from_numpy(x), torch.from_numpy(y)
loader = DataLoader(TensorDataset(x[:500], y[:500]), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))

torch.manual_seed(0)
model = SeqClassifier()
opt = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()

# Write the 10-epoch training loop here

model.eval()
with torch.no_grad():
    acc = (model(x[500:]).argmax(dim=1) == y[500:]).float().mean().item()
print(acc > 0.5, acc > 0.9)
