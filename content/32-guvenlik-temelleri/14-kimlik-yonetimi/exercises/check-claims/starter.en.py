def check_claims(claims, issuer, audience, now):
    if now > claims["exp"]:
        return "expired"
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
