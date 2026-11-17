from torch import nn


def rnn_param_count(kind, input_size, hidden_size):
    # Kodunu buraya yaz
    return 0

print(rnn_param_count("rnn", 4, 3))
print(rnn_param_count("gru", 4, 3))
print(rnn_param_count("lstm", 10, 8))
