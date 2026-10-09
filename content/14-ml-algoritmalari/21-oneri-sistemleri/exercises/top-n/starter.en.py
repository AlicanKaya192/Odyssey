def top_n(scores, ratings, n):
    unseen = [i for i in range(len(scores)) if ratings[i] == 0]
    # Sort by prediction
    return []

scores = [4.2, 3.1, 4.8, 2.0, 4.5, 3.9]
ratings = [0, 5, 4, 0, 0, 0]
print(top_n(scores, ratings, 2))
print(top_n(scores, ratings, 3))
