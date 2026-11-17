from torch import nn


def rnn_param_count(kind, input_size, hidden_size):
    layers = {"rnn": nn.RNN, "gru": nn.GRU, "lstm": nn.LSTM}
    model = layers[kind](input_size, hidden_size, batch_first=True)
    return sum(p.numel() for p in model.parameters())

print(rnn_param_count("rnn", 4, 3))
print(rnn_param_count("gru", 4, 3))
print(rnn_param_count("lstm", 10, 8))
