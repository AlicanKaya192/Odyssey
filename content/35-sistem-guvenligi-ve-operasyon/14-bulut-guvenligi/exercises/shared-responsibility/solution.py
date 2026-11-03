LAYERS = ["data", "identities", "application", "operating system", "network", "physical"]
PROVIDER_FROM = {"IaaS": 4, "PaaS": 3, "SaaS": 2}


def responsibility(model, layer):
    if model not in PROVIDER_FROM or layer not in LAYERS:
        return "unknown"
    if LAYERS.index(layer) < PROVIDER_FROM[model]:
        return "customer"
    return "provider"

for model, layer in [("IaaS", "operating system"), ("PaaS", "operating system"), ("SaaS", "data"), ("SaaS", "kitchen")]:
    print(model, layer, "->", responsibility(model, layer))
