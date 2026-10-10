import argparse
import sqlite3
from decimal import Decimal

ORDERS = [("ada", "19.99"), ("alan", "5.01"), ("ada", "12.50"), ("grace", "40.00")]


def report(argv):
    # argparse, sqlite3, Decimal
    return []

print(report(["--min", "10"]))
print(report(["--customer", "ada"]))
