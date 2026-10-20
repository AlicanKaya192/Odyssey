def should_retrain(alert, months_since, every):
    if alert or months_since >= every:
        return "retrain"
    return "wait"


print(should_retrain(False, 1, 3))
print(should_retrain(True, 1, 3))
print(should_retrain(False, 3, 3))
