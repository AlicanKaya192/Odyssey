The exercise's folder has a T-shirt with a transparent background (`shirt.png`) and three photos (`before1.jpg`, `before2.jpg`, `before3.jpg`; drawn for Odyssey). Let's put the shirt on the person in the photo.

Implement a program that takes **two** command-line arguments: an input image and an output image (both JPEG or PNG). Open the input with `Image.open`, resize and crop it to the shirt's size with `ImageOps.fit` (default settings), overlay the shirt with `photo.paste(shirt, shirt)` (the shirt is both the image and the mask), and save the result to the output with `Image.save`.

Exit via `sys.exit` if there are not exactly two arguments (`Too few command-line arguments` / `Too many command-line arguments`), the input's or output's extension is not `.jpg`, `.jpeg` or `.png` (case-insensitively; `Invalid input` / `Invalid output`), the extensions differ (`Input and output have different extensions`), or the input does not exist (`Input does not exist`). When you run the program, your image appears in the **Output** tab. (In CS50 the file is `shirt.py`.)

Hint: `os.path.splitext("before1.jpg")` gives `('before1', '.jpg')`.

## How to test

The cases CS50 gives; Odyssey runs each one in a separate folder and compares your output and the file you write.

- No input → output (nothing) (exit code 1)
- Command `python cozum.py before1.jpg before2.jpg before3.jpg` → output (nothing) (exit code 1)
- Command `python cozum.py before1.jpg invalid_format.bmp` → output (nothing) (exit code 1)
- Command `python cozum.py before1.jpg after1.png` → output (nothing) (exit code 1)
- Command `python cozum.py non_existent_image.jpg after1.jpg` → output (nothing) (exit code 1)
- Command `python cozum.py before1.jpg after1.jpg` → file written `after1.jpg`
- Command `python cozum.py before2.jpg after2.jpg` → file written `after2.jpg`
- Command `python cozum.py before3.jpg after3.jpg` → file written `after3.jpg`
