def allowed(flow, policy):
    src, dst, port = flow
    # is there a fitting line in the list?
    return True

POLICY = [["internet", "dmz", 443], ["dmz", "servers", 5432],
          ["admin", "servers", "any"]]
for flow in [["internet", "dmz", 443], ["internet", "servers", 5432],
             ["admin", "servers", 22], ["dmz", "servers", 22]]:
    print(*flow, allowed(flow, POLICY))
