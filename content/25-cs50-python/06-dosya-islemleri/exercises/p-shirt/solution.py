import os
import sys

from PIL import Image, ImageOps

EXTENSIONS = (".jpg", ".jpeg", ".png")

if len(sys.argv) < 3:
    sys.exit("Too few command-line arguments")
if len(sys.argv) > 3:
    sys.exit("Too many command-line arguments")

before, after = sys.argv[1], sys.argv[2]
before_ext = os.path.splitext(before)[1].lower()
after_ext = os.path.splitext(after)[1].lower()
if before_ext not in EXTENSIONS:
    sys.exit("Invalid input")
if after_ext not in EXTENSIONS:
    sys.exit("Invalid output")
if before_ext != after_ext:
    sys.exit("Input and output have different extensions")

try:
    photo = Image.open(before)
except FileNotFoundError:
    sys.exit("Input does not exist")

shirt = Image.open("shirt.png")
photo = ImageOps.fit(photo, shirt.size)
photo.paste(shirt, shirt)
photo.save(after)
