def classify_attempt(user, user_role, owner, required_role):
    if user_role < required_role:
        return "vertical"
    return "allowed"

print(classify_attempt("ada", "user", "ada", "user"))
print(classify_attempt("ada", "user", "alan", "user"))
print(classify_attempt("ada", "user", None, "admin"))
print(classify_attempt("grace", "moderator", "alan", "moderator"))
