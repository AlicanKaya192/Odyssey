def risky_routes(routes):
    found = []
    for method, path, changes_state in routes:
        if method in ("GET", "HEAD") and changes_state:
            found.append(path)
    return found

routes = [["GET", "/home", False], ["GET", "/delete-account", True],
          ["POST", "/transfer", True], ["HEAD", "/ping", True]]
print(risky_routes(routes))
