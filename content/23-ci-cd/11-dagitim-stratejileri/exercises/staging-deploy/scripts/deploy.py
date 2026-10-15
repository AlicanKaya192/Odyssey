import sys

target = sys.argv[1]
if "--rollback" in sys.argv:
    print(f"rolling back {target} to the previous package")
else:
    print(f"deploying dist/ to {target}")
