import statistics
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: python cozum.py NUMBER ...")

try:
    numbers = [float(arg) for arg in sys.argv[1:]]
except ValueError:
    sys.exit("Not a number")

print(f"{statistics.mean(numbers):.2f}")
