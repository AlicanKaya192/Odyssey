def release_kind(tests_auto, package_auto, release_auto):
    # Check the conditions in order: tests, then packaging, then releasing.
    pass


print(release_kind(False, False, False))
print(release_kind(True, False, False))
print(release_kind(True, True, False))
print(release_kind(True, True, True))
