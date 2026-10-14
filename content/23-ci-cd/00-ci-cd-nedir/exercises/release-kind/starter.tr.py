def release_kind(tests_auto, package_auto, release_auto):
    # Kosullara sirayla bak: once testler, sonra paketleme, sonra yayin.
    pass


print(release_kind(False, False, False))
print(release_kind(True, False, False))
print(release_kind(True, True, False))
print(release_kind(True, True, True))
