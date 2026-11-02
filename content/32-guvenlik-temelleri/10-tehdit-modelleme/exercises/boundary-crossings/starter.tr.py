def boundary_crossings(flows, zones):
    result = []
    for src, dst in flows:
        if zones[src] != zones[dst]:
            result.append(f"{src}->{dst}")
    return result

zones = {"student": "internet", "web": "dmz", "db": "internal", "worker": "internal"}
flows = [["student", "web"], ["web", "db"], ["worker", "db"], ["db", "backup"]]
for flow in boundary_crossings(flows, zones):
    print(flow)
