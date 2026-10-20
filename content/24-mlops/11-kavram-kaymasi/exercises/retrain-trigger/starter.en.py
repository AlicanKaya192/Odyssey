def should_retrain(alert, months_since, every):
    # Two ways: the alert or the schedule.
    pass


print(should_retrain(False, 1, 3))
print(should_retrain(True, 1, 3))
print(should_retrain(False, 3, 3))
