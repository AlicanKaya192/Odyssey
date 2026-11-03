import posixpath


def safe_path(base, name):
    full = posixpath.normpath(posixpath.join(base, name))
    return full if full.startswith(base + "/") else None

BASE = "/srv/app/uploads"
for name in ["cat.png", "../settings.ini", "a/../../x", "/etc/x"]:
    print(name, safe_path(BASE, name))
