def should_run(branch, files, branches, ignored_dirs):
    # Once dala, sonra dosyalara bak.
    pass


print(should_run("main", ["docs/setup.md"], ["main"], ["docs"]))
print(should_run("main", ["docs/setup.md", "app/core.py"], ["main"], ["docs"]))
print(should_run("main", ["README.md"], ["main"], ["docs"]))
print(should_run("feature/login", ["app/core.py"], ["main"], ["docs"]))
