def wheel_filename(name, version):
    clean = ""
    for char in name.lower():
        if char in "-_.":
            if not clean.endswith("_"):
                clean += "_"
        else:
            clean += char
    return clean + "-" + version + "-py3-none-any.whl"


print(wheel_filename("greeter", "0.1.0"))
print(wheel_filename("My-Package", "1.0"))
print(wheel_filename("data.tools", "2.3.1"))
print(wheel_filename("a__b--c", "0.0.1"))
