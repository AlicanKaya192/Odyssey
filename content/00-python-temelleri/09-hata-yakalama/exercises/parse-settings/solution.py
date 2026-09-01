def parse_line(line):
    if "=" not in line:
        raise ValueError("bad line: " + line)
    key, value = line.split("=", 1)
    return key, value


lines = ["name=Ada", "broken", "city=London"]
settings = {}

for line in lines:
    try:
        key, value = parse_line(line)
    except ValueError as error:
        print(error)
    else:
        settings[key] = value


print(settings)
