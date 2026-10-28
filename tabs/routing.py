"""Smooth routes between bike lane streets, along Heilbronn's real road network."""
from functools import lru_cache

import networkx as nx

from tabs.real_data import NETWORK, BIKE_STREETS, BUMPY_ROADS, parse_linestring, distance_m, line_length_m

# A meter on a bumpy road counts like this many meters on a smooth road,
# so routes go around bumpy roads unless there is no other way
BUMPY_PENALTY = 10
BUMPY_NAMES = {r["name"] for r in BUMPY_ROADS}


def node(point):
    """Crossings are where pieces share an end point; rounding makes equal points match."""
    return (round(point[0], 6), round(point[1], 6))


# ─── Build the road graph once: crossings are nodes, street pieces are edges ───
GRAPH = nx.Graph()
STREET_NODES = {}  # street name -> all crossings on that street
for names, wkt in zip(NETWORK["names"], NETWORK["geometry_wkt"]):
    points = parse_linestring(wkt)
    a, b = node(points[0]), node(points[-1])
    for name in names:
        STREET_NODES.setdefault(name, set()).update([a, b])
    length = line_length_m(points)
    bumpy = any(n in BUMPY_NAMES for n in names)
    cost = length * (BUMPY_PENALTY if bumpy else 1)
    # two pieces between the same crossings: keep the cheaper one
    if GRAPH.has_edge(a, b) and GRAPH[a][b]["cost"] <= cost:
        continue
    GRAPH.add_edge(a, b, cost=cost, length=length, points=points, names=names, bumpy=bumpy)


def bike_street_nodes(street):
    """Crossings of a bike street ("A & B" means both streets)."""
    nodes = set()
    for name in street["name"].split(" & "):
        nodes |= STREET_NODES.get(name, set())
    return nodes


@lru_cache(maxsize=None)
def route_to_nearest_bike_street(street_name):
    """Smoothest route from this bike street to the nearest other bike street.

    Returns a dict with: target, lines (list of [lat, lon] point lists), length_m,
    streets (other streets on the way), uses_bumpy. Returns None if no route exists.
    """
    start = next(s for s in BIKE_STREETS if s["name"] == street_name)
    sources = bike_street_nodes(start)
    # every crossing of every other bike street is a possible goal
    goals = {}
    for other in BIKE_STREETS:
        if other["name"] != street_name:
            for n in bike_street_nodes(other) - sources:
                goals[n] = other["name"]
    if not sources or not goals:
        return None

    costs, paths = nx.multi_source_dijkstra(GRAPH, sources, weight="cost")
    reachable = [n for n in goals if n in costs]
    if not reachable:
        return None
    goal = min(reachable, key=lambda n: costs[n])

    ends = set(street_name.split(" & ")) | set(goals[goal].split(" & "))
    return describe_route(paths[goal], goals[goal], ends)


def describe_route(path, target, skip_names):
    """Turn a list of crossings into the route dict (see route_to_nearest_bike_street)."""
    edges = [GRAPH[a][b] for a, b in zip(path, path[1:])]
    # street names on the way, in order, without the names in skip_names
    streets = []
    for e in edges:
        for name in e["names"]:
            if name not in streets and name not in skip_names:
                streets.append(name)
    return {
        "target": target,
        "lines": [e["points"] for e in edges],
        "length_m": sum(e["length"] for e in edges),
        "streets": streets,
        "uses_bumpy": any(e["bumpy"] for e in edges),
    }


@lru_cache(maxsize=1)
def routes_from_all_bike_streets():
    """One search outward from every bike street at once.

    Returns (start_street, costs, paths): for every crossing in the city, costs says how
    far its nearest bike street is, and paths the route from that bike street to it.
    start_street tells which bike street a route starts on.
    """
    start_street = {}
    for street in BIKE_STREETS:
        for n in bike_street_nodes(street):
            start_street.setdefault(n, street["name"])
    costs, paths = nx.multi_source_dijkstra(GRAPH, set(start_street), weight="cost")
    return start_street, costs, paths


@lru_cache(maxsize=None)
def route_from_area_to_nearest_bike_street(lat, lon, radius_m):
    """Smoothest route from an area (its circle) to the nearest bike street.

    Starts from the crossing inside the circle that is closest to a bike street
    (or the crossing nearest the center if none is inside). Same dict as above, or None.
    """
    start_street, costs, paths = routes_from_all_bike_streets()
    center = (lat, lon)
    inside = [n for n in GRAPH.nodes if distance_m(*center, *n) <= radius_m]
    if not inside:
        inside = [min(GRAPH.nodes, key=lambda n: distance_m(*center, *n))]
    reachable = [n for n in inside if n in costs]
    if not reachable:
        return None
    best = min(reachable, key=lambda n: costs[n])
    path = paths[best][::-1]  # the search ran from the bike street, so turn it around
    target = start_street[path[-1]]
    return describe_route(path, target, set(target.split(" & ")))
