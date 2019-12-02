msat_vals = [1_000, 1_000_000, 1_000_000_000]
fuzz_vals = [0, 0.5, 1]


# Probing function
def probe_route(msat_vals, fuzz_vals):
    route_set = []
    for msat in msat_vals:
        for fuzz in fuzz_vals:
            route = Route(rpc_object.getroute(fromid="A", node_id="B", msatoshi=msat, fuzzpercent=fuzz))
            if route not in route_set:
                route_set.append(route)
    return route_set
