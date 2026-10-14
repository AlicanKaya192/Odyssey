def wheel_filename(name, version):
    # Go through the name letter by letter and build a clean name.
    pass


print(wheel_filename("greeter", "0.1.0"))
print(wheel_filename("My-Package", "1.0"))
print(wheel_filename("data.tools", "2.3.1"))
print(wheel_filename("a__b--c", "0.0.1"))
