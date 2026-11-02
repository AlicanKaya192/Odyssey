PROPERTIES = {
    "S": "authenticity", "T": "integrity", "R": "non-repudiation",
    "I": "confidentiality", "D": "availability", "E": "authorization",
}


def stride_property(letter):
    return PROPERTIES.get(letter.upper())

for letter in ["S", "t", "I", "e", "X"]:
    print(letter, stride_property(letter))
