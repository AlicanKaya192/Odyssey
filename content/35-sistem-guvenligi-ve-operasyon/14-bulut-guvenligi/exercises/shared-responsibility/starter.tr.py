LAYERS = ["data", "identities", "application", "operating system", "network", "physical"]
PROVIDER_FROM = {"IaaS": 4, "PaaS": 3, "SaaS": 2}


def responsibility(model, layer):
    # LAYERS.index(layer) ve PROVIDER_FROM[model]
    return "unknown"

for model, layer in [("IaaS", "operating system"), ("PaaS", "operating system"), ("SaaS", "data"), ("SaaS", "kitchen")]:
    print(model, layer, "->", responsibility(model, layer))
