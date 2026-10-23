from fpdf import FPDF


def main():
    name = input("Name: ")
    make_shirtificate(name)


def make_shirtificate(name):
    pdf = FPDF(orientation="P", format="A4")
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.set_font("helvetica", "B", 42)
    pdf.cell(0, 50, "CS50 Shirtificate", align="C")
    width = 180
    pdf.image("shirtificate.png", x=(pdf.w - width) / 2, y=70, w=width)
    pdf.set_font_size(24)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, 120)
    pdf.cell(pdf.w, 10, f"{name} took CS50", align="C")
    pdf.output("shirtificate.pdf")


if __name__ == "__main__":
    main()
