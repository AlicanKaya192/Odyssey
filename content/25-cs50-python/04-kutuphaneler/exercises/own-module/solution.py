import sys

from shapes import cube, square

if len(sys.argv) != 2:
    sys.exit("Usage: python cozum.py NUMBER")

n = int(sys.argv[1])
print(square(n), cube(n))
