def risk_score(likelihood, impact):
    if not 1 <= likelihood <= 5 or not 1 <= impact <= 5:
        return None
    return likelihood * impact

print(risk_score(4, 3))
print(risk_score(5, 5))
print(risk_score(0, 3))
print(risk_score(2, 6))
