import sys

from PIL import Image

if len(sys.argv) < 3:
    sys.exit("Usage: python cozum.py FRAME FRAME ...")

frames = []
for name in sys.argv[1:]:
    frames.append(Image.open(name))

frames[0].save("animation.gif", save_all=True, append_images=frames[1:], duration=200, loop=0)
