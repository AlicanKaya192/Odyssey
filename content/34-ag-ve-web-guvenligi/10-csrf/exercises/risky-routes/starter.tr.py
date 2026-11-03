def risky_routes(routes):
    found = []
    # GET ya da HEAD olup durum degistirenler
    return found

routes = [["GET", "/home", False], ["GET", "/delete-account", True],
          ["POST", "/transfer", True], ["HEAD", "/ping", True]]
print(risky_routes(routes))
