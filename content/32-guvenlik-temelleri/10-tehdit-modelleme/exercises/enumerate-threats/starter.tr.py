PER_ELEMENT = {"external_entity": "SR", "process": "STRIDE",
               "data_store": "TRID", "data_flow": "TID"}


def enumerate_threats(elements):
    threats = []
    for name, kind in elements:
        for letter in PER_ELEMENT[kind]:
            threats.append(f"{name}:{letter}")
    return threats

system = [["student", "external_entity"], ["login", "data_flow"], ["plugin", "unknown"]]
threats = enumerate_threats(system)
print(len(threats))
for threat in threats:
    print(threat)
