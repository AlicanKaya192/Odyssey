def check_claims(claims, issuer, audience, now):
    if claims.get("iss") != issuer:
        return "bad-issuer"
    if claims.get("aud") != audience:
        return "bad-audience"
    if now >= claims.get("exp", 0):
        return "expired"
    if now < claims.get("nbf", now):
        return "not-yet-valid"
    return "ok"

ISSUER = "https://id.school.example"
claims = {
    "iss": ISSUER,
    "aud": "grades-app",
    "sub": "ada",
    "exp": 1000,
    "nbf": 100,
}
for now in [50, 500, 1000]:
    print(now, check_claims(claims, ISSUER, "grades-app", now))
print(check_claims(claims, ISSUER, "library-app", 500))
