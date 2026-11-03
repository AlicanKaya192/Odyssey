def risky_routes(routes):
    found = []
    # GET or HEAD and changing state
    return found

routes = [["GET", "/home", False], ["GET", "/delete-account", True],
          ["POST", "/transfer", True], ["HEAD", "/ping", True]]
print(risky_routes(routes))
