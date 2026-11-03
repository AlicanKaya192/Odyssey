def unpinned(lines):
    return [line for line in lines if "==" not in line]

LINES = [
    "numpy==2.1.3",
    "pandas>=2.0",
    "",
    "# tools",
    "flask",
    "pytest==8.3.4  # tests",
    "httpkit~=1.0",
]
print(unpinned(LINES))
