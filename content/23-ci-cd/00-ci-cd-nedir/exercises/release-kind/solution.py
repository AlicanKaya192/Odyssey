def release_kind(tests_auto, package_auto, release_auto):
    if not tests_auto:
        return "manual"
    if not package_auto:
        return "continuous integration"
    if not release_auto:
        return "continuous delivery"
    return "continuous deployment"


print(release_kind(False, False, False))
print(release_kind(True, False, False))
print(release_kind(True, True, False))
print(release_kind(True, True, True))
