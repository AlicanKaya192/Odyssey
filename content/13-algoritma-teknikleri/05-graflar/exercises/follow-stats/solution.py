def follow_stats(follows):
    followers, following = {}, {}
    for a, b in follows:
        following.setdefault(a, set()).add(b)
        followers.setdefault(b, set()).add(a)
    people = sorted(set(followers) | set(following))
    return {p: [len(followers.get(p, ())), len(following.get(p, ()))] for p in people}


follows = [["ada", "bora"], ["cem", "bora"], ["deniz", "bora"],
           ["bora", "ece"], ["ada", "ece"], ["ece", "ada"]]
for person, (fans, follows_count) in follow_stats(follows).items():
    print(person, fans, follows_count)
