def sends_cookie(samesite, cross_site, method, top_level):
    if not cross_site:
        return True
    if samesite == "Strict":
        return False
    if samesite == "Lax":
        return method == "GET" and top_level
    return True

for samesite, cross, method, top in [["Strict", True, "GET", True],
                                     ["Lax", True, "POST", False],
                                     ["Lax", True, "GET", True],
                                     ["Lax", False, "POST", False],
                                     ["None", True, "POST", False]]:
    print(samesite, method, sends_cookie(samesite, cross, method, top))
