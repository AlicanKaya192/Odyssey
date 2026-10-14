def should_run(branch, files, branches, ignored_dirs):
    if branch not in branches:
        return False
    for path in files:
        if path.split("/")[0] not in ignored_dirs:
            return True
    return False


print(should_run("main", ["docs/setup.md"], ["main"], ["docs"]))
print(should_run("main", ["docs/setup.md", "app/core.py"], ["main"], ["docs"]))
print(should_run("main", ["README.md"], ["main"], ["docs"]))
print(should_run("feature/login", ["app/core.py"], ["main"], ["docs"]))
