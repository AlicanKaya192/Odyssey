def parse_line(line):
    word, *numbers = line.split()
    return [word, [float(x) for x in numbers]]

word, numbers = parse_line("cat 0.1250 -0.5000 2.0000")
print(word, numbers)
