def boundary_crossings(flows, zones):
    result = []
    for src, dst in flows:
        a, b = zones.get(src), zones.get(dst)
        if a is None or b is None or a != b:
            result.append(f"{src}->{dst}")
    return result

zones = {"student": "internet", "web": "dmz", "db": "internal", "worker": "internal"}
flows = [["student", "web"], ["web", "db"], ["worker", "db"], ["db", "backup"]]
for flow in boundary_crossings(flows, zones):
    print(flow)
