from torch import nn


def classifier_params(vocab, dim, hidden):
    # Build the embedding, LSTM and linear layer, count the parameters
    return 0

print(classifier_params(10, 8, 16))
print(classifier_params(100, 4, 4))
