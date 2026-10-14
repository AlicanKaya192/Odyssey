def feedback_minutes(stages):
    total = 0
    for name, minutes, passed in stages:
        total = total + minutes
        if not passed:
            return total
    return total


slow_first = [("test", 8, True), ("build", 5, True), ("lint", 1, False)]
fast_first = [("lint", 1, False), ("build", 5, True), ("test", 8, True)]
print("slow first:", feedback_minutes(slow_first))
print("fast first:", feedback_minutes(fast_first))
print("all pass:", feedback_minutes([("lint", 1, True), ("test", 8, True)]))
