import hashlib


def changed_files(files, manifest):
    changed = []
    for name in manifest:
        if name not in files:
            changed.append(name)
    return sorted(changed)

manifest = {'app.py': 'c2d0a5e0790d97a015387a995c0d0b5eb3e88138466586fc980787c9b1731eb8', 'config.json': '91b415068e9e02958c86464025e0c061ed4e6df05b175751c9fa627e9983e989', 'readme.md': '29215b5404a64a82b1f244847bd104de4be5d0f0b04f14e95f1355a013344b50'}
files = {'app.py': "print('hi')", 'config.json': '{"debug": true}'}
print(changed_files(files, manifest))
