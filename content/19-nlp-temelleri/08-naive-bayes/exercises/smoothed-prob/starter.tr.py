def word_prob(count, class_total, vocab_size, alpha):
    return count / class_total

print(word_prob(0, 1000, 300, 1.0))
print(word_prob(25, 1000, 300, 1.0))
print(word_prob(25, 1000, 300, 0.1))
