RANK = {"user": 1, "moderator": 2, "admin": 3}


def classify_attempt(user, user_role, owner, required_role):
    if RANK[user_role] < RANK[required_role]:
        return "vertical"
    if owner is not None and owner != user and user_role == "user":
        return "horizontal"
    return "allowed"

print(classify_attempt("ada", "user", "ada", "user"))
print(classify_attempt("ada", "user", "alan", "user"))
print(classify_attempt("ada", "user", None, "admin"))
print(classify_attempt("grace", "moderator", "alan", "moderator"))
