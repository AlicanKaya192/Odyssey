def phishing_score(mail, weights, threshold):
    score = sum(weights[sign] for sign in mail)
    return (score, "report" if score > threshold else "ok")

weights = {"urgent": 2, "asks_password": 3, "link_mismatch": 3, "attachment": 1}
mail = {"urgent": True, "asks_password": False, "link_mismatch": True}
print(phishing_score(mail, weights, 4))
print(phishing_score({}, weights, 4))
