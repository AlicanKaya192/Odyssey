Ask the user for their name and create a shirt certificate, `shirtificate.pdf`, with `fpdf2` (installed in Odyssey, `from fpdf import FPDF`). Requirements:

- The page is **portrait A4** (210 × 297 mm), a single page.
- At the top of the page, `CS50 Shirtificate`, centered horizontally.
- The shirt image `shirtificate.png` in the folder, centered horizontally (`pdf.image`).
- On top of the shirt, in **white** text, `Name took CS50` (`Harry took CS50`).

Borders, colors and lines are up to you; long names do not need to fit on the line. Odyssey checks the PDF's page, texts, text color and whether the image is centered; it does not compare its look exactly.

## How to test

- Input `Harry` → file written `shirtificate.pdf`
- Input `Ada Lovelace` → file written `shirtificate.pdf`
