def allowed(flow, policy):
    src, dst, port = flow
    for p_src, p_dst, p_port in policy:
        if p_src == src and p_dst == dst and p_port in ("any", port):
            return True
    return False

POLICY = [["internet", "dmz", 443], ["dmz", "servers", 5432],
          ["admin", "servers", "any"]]
for flow in [["internet", "dmz", 443], ["internet", "servers", 5432],
             ["admin", "servers", 22], ["dmz", "servers", 22]]:
    print(*flow, allowed(flow, POLICY))
