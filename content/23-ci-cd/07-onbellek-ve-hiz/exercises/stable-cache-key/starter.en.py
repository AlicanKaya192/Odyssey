import hashlib


def cache_key(tool, runner_os, requirements):
    # First clean and sort the lines, then take the hash.
    pass


a = "pytest==8.4.2\nrequests==2.32.5\n"
b = "requests==2.32.5\n\npytest==8.4.2\n"
c = "pytest==8.4.2\nrequests==2.32.6\n"
print(cache_key("pip", "Linux", a))
print(cache_key("pip", "Linux", b))
print(cache_key("pip", "Linux", c))
