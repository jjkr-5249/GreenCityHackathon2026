"""All real data the app shows: measured areas, sensor bike tracks, bike streets and bumpy roads.

The CSV files are read once from the csv/ folder in the project root. Everything below is
plain data (DataFrames, lists of dicts) that the tabs import, so no tab reads a file itself.
"""
import ast
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
import pandas as pd

# tabs/real_data.py -> project root -> csv/
DATA_DIR = Path(__file__).resolve().parent.parent / "csv"


def distance_m(lat1, lon1, lat2, lon2):
    """Distance in meters between two points on Earth (haversine formula)."""
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371000 * asin(sqrt(a))

# ─── Real measurements: openSenseMap bike sensors, Dec 2025 - Oct 2026 ───
# One row per area. Columns:
#   rank_overall   1 = coolest and cleanest area, 18 = hottest and dirtiest
#   temp_anom      °C above (+) or below (-) the median of all sensors at the same hour
#   pm25_anom      PM2.5 µg/m³ above the median of all sensors at the same hour
#   temp_mean, pm25_mean, pm10_mean   plain averages
#   readings, days, riders            how much data each area has
#   lat, lon       map position: the median of the area's GPS points
#   label          short name for the map
AREAS = pd.read_csv(DATA_DIR / "heilbronn_area_ranking.csv")

AREA_RADIUS_M = 450  # radius of the measured-area circles on the map (meters)
AREA_NAMES = AREAS["area"].tolist()  # used as locations in the forms
MARKTPLATZ = [49.1422, 9.2190]       # map center when nothing is selected


def weighted_mean(column):
    """Average over all areas, weighted by how many readings each area has."""
    return (AREAS[column] * AREAS["readings"]).sum() / AREAS["readings"].sum()

# Where the sensor bikes rode: GPS points grouped into cells of about 55 m
#   lat, lon   center of the cell
#   n          number of readings in the cell
TRACKS = pd.read_csv(DATA_DIR / "tracks.csv")

# Streets with the most bike infrastructure
#   segments   number of street sections with this bike infrastructure
#   type       "lane" = own painted bike lane, "shared_lane" = bikes share the lane with cars
BIKE_STREETS = [
    {"name": "Neckargartacher Straße", "area": "Central / West Corridor",
     "lat": 49.1464, "lon": 9.1955, "segments": 60, "type": "shared_lane"},
    {"name": "Karlstraße", "area": "East-West City Center Axis",
     "lat": 49.1426, "lon": 9.2304, "segments": 38, "type": "lane"},
    {"name": "Würzburger Straße", "area": "Northwest Sector / Frankenbach",
     "lat": 49.1628, "lon": 9.1769, "segments": 26, "type": "lane"},
    {"name": "Donnbronner Straße", "area": "Southeast Corner / Flein towards Donnbronn",
     "lat": 49.1174, "lon": 9.2692, "segments": 26, "type": "shared_lane"},
    {"name": "Bismarckstraße & Jägerhausstraße", "area": "East Inner City Corridor",
     "lat": 49.1401, "lon": 9.2373, "segments": 26, "type": "lane"},
    {"name": "Gottlieb-Daimler-Straße", "area": "North Industrial Area",
     "lat": 49.1545, "lon": 9.2136, "segments": 25, "type": "lane"},
    {"name": "Salzstraße", "area": "North Industrial / Port Corridor",
     "lat": 49.1638, "lon": 9.2159, "segments": 24, "type": "lane"},
    {"name": "Schlossstraße", "area": "Far West Sector / Kirchhausen",
     "lat": 49.1825, "lon": 9.1122, "segments": 22, "type": "shared_lane"},
    {"name": "Charlottenstraße", "area": "South City Core",
     "lat": 49.1220, "lon": 9.2167, "segments": 14, "type": "lane"},
]

# Bumpy roads: how rough the ride is (higher score = bumpier)
#   avg_rough    average roughness score of the street
#   peak_rough   worst roughness score measured on the street
#   segments     number of street sections with roughness data
BUMPY_ROADS = [
    {"name": "Rolandstraße", "avg_rough": 79.79, "peak_rough": 100.0, "segments": 4},
    {"name": "Hirschstraße", "avg_rough": 48.69, "peak_rough": 100.0, "segments": 18},
    {"name": "Zückwolfstraße", "avg_rough": 46.67, "peak_rough": 100.0, "segments": 6},
    {"name": "Gustav-Binder-Straße", "avg_rough": 40.00, "peak_rough": 40.0, "segments": 2},
    {"name": "Virchowstraße", "avg_rough": 40.00, "peak_rough": 40.0, "segments": 1},
    {"name": "Tränkgasse", "avg_rough": 40.00, "peak_rough": 40.0, "segments": 4},
    {"name": "Steubenstraße", "avg_rough": 40.00, "peak_rough": 40.0, "segments": 3},
    {"name": "Kurze Straße", "avg_rough": 40.00, "peak_rough": 40.0, "segments": 2},
    {"name": "Theodor-Heuss-Straße", "avg_rough": 38.47, "peak_rough": 40.0, "segments": 12},
    {"name": "Im Kohlpfad", "avg_rough": 37.67, "peak_rough": 40.0, "segments": 4},
    {"name": "Dittmarstraße", "avg_rough": 37.03, "peak_rough": 40.0, "segments": 26},
]

# Heilbronn's road network from OpenStreetMap: one row per piece of street
#   name           street name
#   cycleway       bike infrastructure ("lane", "shared_lane", ...)
#   geometry_wkt   the course of the street: "LINESTRING (lon lat, lon lat, ...)"
NETWORK = pd.read_csv(DATA_DIR / "bike_road_network_heilbronn.csv",
                      usecols=["name", "cycleway", "geometry_wkt"])


def split_names(name):
    """A piece can belong to several streets, written as "['A', 'B']". Return a list of names."""
    if not isinstance(name, str):
        return []  # piece without a name
    if name.startswith("["):
        return ast.literal_eval(name)
    return [name]


#   names   the piece's street names as a list
NETWORK["names"] = NETWORK["name"].map(split_names)


def parse_linestring(wkt):
    """'LINESTRING (9.15 49.11, 9.16 49.12)' -> [[49.11, 9.15], [49.12, 9.16]] (lat first, for folium)."""
    inside = wkt[wkt.index("(") + 1 : wkt.rindex(")")]
    points = []
    for pair in inside.split(","):
        lon, lat = pair.split()
        points.append([float(lat), float(lon)])
    return points


def street_lines(names):
    """All pieces of the streets with these names, each piece a list of [lat, lon] points."""
    on_street = NETWORK["names"].map(lambda piece_names: any(n in names for n in piece_names))
    pieces = NETWORK[on_street]["geometry_wkt"]
    return [parse_linestring(wkt) for wkt in pieces]


# Give each bike street its real course from the network
#   lines    list of pieces, each piece is a list of [lat, lon] points
#   points   all points of the street together
# "Bismarckstraße & Jägerhausstraße" means both streets
for street in BIKE_STREETS:
    street["lines"] = street_lines(street["name"].split(" & "))
    street["points"] = [p for line in street["lines"] for p in line]

# Same for each bumpy road, plus
#   lat, lon   middle of the street (where its bike sign goes), None if not in the network
for road in BUMPY_ROADS:
    road["lines"] = street_lines([road["name"]])
    road["points"] = [p for line in road["lines"] for p in line]
    if road["points"]:
        road["lat"] = sum(p[0] for p in road["points"]) / len(road["points"])
        road["lon"] = sum(p[1] for p in road["points"]) / len(road["points"])
    else:
        road["lat"], road["lon"] = None, None

# Only bumpy roads found in the road network can go on the map
BUMPY_ON_MAP = [r for r in BUMPY_ROADS if r["lat"] is not None and r["lon"] is not None]

# ─── Accessible routes: the bike streets, checked with the sensor bikes ───
# A piece of a bike street counts as accessible when:
#   - the sensor bikes rode along most of it, so it has a rideable surface
#   - it is not part of a bumpy road
LAT_STEP, LON_STEP = 0.0005, 0.00075  # cell size in tracks.csv (about 55 m)
MIN_RIDES = 20          # cells with fewer readings may be GPS noise
MIN_RIDDEN_SHARE = 0.5  # at least this part of a piece must lie on ridden cells
SAMPLE_M = 20           # a piece is checked every 20 m


def cell_of(lat, lon):
    """Grid position (row, col) of the tracks.csv cell that contains the point."""
    return (round(lat / LAT_STEP), round(lon / LON_STEP))


# Cells the sensor bikes rode through often
RIDDEN = {cell_of(lat, lon) for lat, lon, n in TRACKS[["lat", "lon", "n"]].itertuples(index=False)
          if n >= MIN_RIDES}


def is_ridden(lat, lon):
    """True if the point lies in a cell the bikes rode often."""
    return cell_of(lat, lon) in RIDDEN


def line_length_m(line):
    """Length in meters of a piece given as [lat, lon] points."""
    return sum(distance_m(*p, *q) for p, q in zip(line, line[1:]))


def ridden_share(line):
    """Part of the piece (0 to 1) that lies on ridden cells, checked every SAMPLE_M meters."""
    samples = []
    for p, q in zip(line, line[1:]):
        steps = max(1, int(distance_m(*p, *q) // SAMPLE_M))
        for i in range(steps):
            f = i / steps
            samples.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))
    samples.append(tuple(line[-1]))
    return sum(is_ridden(*s) for s in samples) / len(samples)


BUMPY_LINES = [line for road in BUMPY_ROADS for line in road["lines"]]

# Add to each bike street
#   access_lines   its accessible pieces (empty = the sensor bikes never rode there)
#   length_km      length of all its pieces
#   access_km      length of the accessible pieces
for street in BIKE_STREETS:
    street["access_lines"] = [line for line in street["lines"]
                              if line not in BUMPY_LINES and ridden_share(line) >= MIN_RIDDEN_SHARE]
    street["length_km"] = sum(line_length_m(line) for line in street["lines"]) / 1000
    street["access_km"] = sum(line_length_m(line) for line in street["access_lines"]) / 1000

# How the ranking was made
DATA_INFO = {
    "points": 416880,
    "sensors": 26,
    "first_day": "2025-12-14",
    "last_day": "2026-10-19",
    "max_km": 2.5,        # readings further than this from an area were not used
    "min_readings": 300,  # areas with fewer readings were left out
    "min_days": 3,        # areas measured on fewer days were left out
    "max_humidity": 85,   # readings above this humidity were left out
}
