Login and `current_user` are ready; in the `roles` dictionary `ada` is an
admin and `alan` a member.

**What to do:**

1. `require_admin`: depends on `current_user`; `403` (`"Admins only"`) if
   the role isn't `admin`.
2. `GET /admin/users` → the sorted list of usernames; admins only.

- no token → `401`
- `alan`'s token → `403`
- `ada`'s token → `["ada", "alan"]`
