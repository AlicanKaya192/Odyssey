def can_edit_post(user, role, post):
    return role in ("admin", "moderator", "user")

post = {"id": 7, "author": "ada", "locked": False}
locked = {"id": 8, "author": "ada", "locked": True}
for user, role in [("ada", "user"), ("alan", "user"), ("grace", "moderator")]:
    print(user, can_edit_post(user, role, post), can_edit_post(user, role, locked))
