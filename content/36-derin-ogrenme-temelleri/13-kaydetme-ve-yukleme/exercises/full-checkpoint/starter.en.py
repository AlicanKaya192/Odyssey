import torch
from torch import nn

X = torch.randn(32, 4, generator=torch.Generator().manual_seed(5))
Y = torch.arange(32) % 3


def make():
    torch.manual_seed(0)
    net = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
    return net, torch.optim.Adam(net.parameters(), lr=0.01)


def train(net, optimizer, epochs):
    for _ in range(epochs):
        optimizer.zero_grad()
        nn.functional.cross_entropy(net(X), Y).backward()
        optimizer.step()


def resume_matches():
    net, optimizer = make()
    train(net, optimizer, 6)
    straight = net[0].weight.clone()

    net, optimizer = make()
    train(net, optimizer, 3)
    torch.save({"model": net.state_dict()}, "checkpoint.pt")

    checkpoint = torch.load("checkpoint.pt", weights_only=True)
    net, optimizer = make()
    net.load_state_dict(checkpoint["model"])
    train(net, optimizer, 3)
    return torch.equal(straight, net[0].weight)

print(resume_matches())
