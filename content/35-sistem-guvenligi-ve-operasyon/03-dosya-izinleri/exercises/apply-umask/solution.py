def apply_umask(base, umask):
    return base & ~umask

for base, umask in [(0o666, 0o022), (0o666, 0o077), (0o777, 0o027)]:
    print(oct(apply_umask(base, umask)))
