"""All real data the app shows: measured areas (overall and per month), sensor bike tracks,
bike streets and bumpy roads.
 
The files in the csv/ folder are read once. The measurement files are made from the raw
openSenseMap readings by prepare_data.py ("make data"), see that file for the rules.
Everything below is plain data (DataFrames, lists of dicts) that the tabs import,
so no tab reads a file itself.
"""
import ast
import json
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
 
 
def line_length_m(line):
    """Length in meters of a piece given as [lat, lon] points."""
    return sum(distance_m(*p, *q) for p, q in zip(line, line[1:]))
 
 
# ─── Real measurements: openSenseMap bike sensors ───
# AREAS: one row per area, all months together. Columns:
#   rank_overall   1 = coolest and cleanest area
#   rank_temp, rank_air   1 = coolest / cleanest
#   temp_anom      °C above (+) or below (-) the median of all sensors at the same hour
#   pm25_anom      PM2.5 µg/m³ above the median of all sensors at the same hour
#   temp_mean, pm25_mean, pm10_mean   plain averages
#   readings, days, riders            how much data each area has; first, last = first and last day
#   lat, lon       fixed area center (area_centers.csv);  label = short name for the map
AREAS = pd.read_csv(DATA_DIR / "heilbronn_area_ranking.csv")
 
# MONTHS: the same columns, one row per area and month ("2026-06", ...), plus
#   enough_data    True if the area has enough readings and days that month
#   ranks are only among the areas with enough data that month
MONTHS = pd.read_csv(DATA_DIR / "area_months.csv")
 
# Rules and totals of the data preparation (points, sensors, first_day, last_day, months, month_totals, ...)
DATA_INFO = json.loads((DATA_DIR / "data_info.json").read_text())
 
AREA_RADIUS_M = 450  # radius of the measured-area circles on the map (meters)
AREA_NAMES = AREAS["area"].tolist()  # used as locations in the forms
MARKTPLATZ = [49.1422, 9.2190]       # map center when nothing is selected
 
 
def weighted_mean(table, column):
    """Average over the areas in table, weighted by how many readings each has (None if empty)."""
    if table.empty:
        return None
    return (table[column] * table["readings"]).sum() / table["readings"].sum()
 
 
# Where the sensor bikes rode, per month: GPS points grouped into cells of about 55 m
#   month      like "2026-06"
#   lat, lon   center of the cell
#   n          number of readings in the cell
TRACKS = pd.read_csv(DATA_DIR / "tracks.csv")
TRACKS_ALL = TRACKS.groupby(["lat", "lon"], as_index=False)["n"].sum()  # all months added up
 
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
 
 
def street_pieces(names):
    """The rows of NETWORK that belong to any of these street names."""
    return NETWORK[NETWORK["names"].map(lambda piece_names: any(n in names for n in piece_names))]
 
 
def add_course(street, pieces):
    """Give a street its real course from the network:
        lines      list of pieces, each piece is a list of [lat, lon] points
        points     all points of the street together
        lat, lon   middle of the street (where its bike sign goes), None if not in the network
    """
    street["lines"] = [parse_linestring(wkt) for wkt in pieces["geometry_wkt"]]
    street["points"] = [p for line in street["lines"] for p in line]
    if street["points"]:
        street["lat"] = sum(p[0] for p in street["points"]) / len(street["points"])
        street["lon"] = sum(p[1] for p in street["points"]) / len(street["points"])
    else:
        street["lat"], street["lon"] = None, None
 
 
def course_of(name):
    """Any street by its name, with its course from the network (see add_course)."""
    street = {"name": name}
    add_course(street, street_pieces([name]))
    return street
 
 
# Streets with the most bike infrastructure. Taken from the network:
#   type       the street's bike infrastructure: "lane" = own painted bike lane,
#              "shared_lane" = bikes share the lane with cars
#   segments   number of street pieces with that bike infrastructure
# "Bismarckstraße & Jägerhausstraße" means both streets
BIKE_STREETS = [
    {"name": "Neckargartacher Straße", "area": "Central / West Corridor"},
    {"name": "Karlstraße", "area": "East-West City Center Axis"},
    {"name": "Würzburger Straße", "area": "Northwest Sector / Frankenbach"},
    {"name": "Donnbronner Straße", "area": "Southeast Corner / Flein towards Donnbronn"},
    {"name": "Bismarckstraße & Jägerhausstraße", "area": "East Inner City Corridor"},
    {"name": "Gottlieb-Daimler-Straße", "area": "North Industrial Area"},
    {"name": "Salzstraße", "area": "North Industrial / Port Corridor"},
    {"name": "Schlossstraße", "area": "Far West Sector / Kirchhausen"},
    {"name": "Charlottenstraße", "area": "South City Core"},
]
for street in BIKE_STREETS:
    pieces = street_pieces(street["name"].split(" & "))
    add_course(street, pieces)
    counts = pieces["cycleway"].value_counts()  # most common bike infrastructure first, e.g. lane: 38
    street["type"], street["segments"] = counts.index[0], int(counts.iloc[0])
 
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
for road in BUMPY_ROADS:
    add_course(road, street_pieces([road["name"]]))
 
# Only bumpy roads found in the road network can go on the map
BUMPY_ON_MAP = [r for r in BUMPY_ROADS if r["lat"] is not None]
 
# ─── Accessible routes: the bike streets, checked with the sensor bikes ───
# A piece of a bike street counts as accessible when:
#   - the sensor bikes rode along most of it, so it has a rideable surface
#   - it is not part of a bumpy road
CELL_LAT, CELL_LON = 0.0005, 0.00075  # cell size in tracks.csv (about 55 m), must match prepare_data.py
MIN_RIDES = 20          # cells with fewer readings (all months together) may be GPS noise
MIN_RIDDEN_SHARE = 0.5  # at least this part of a piece must lie on ridden cells
SAMPLE_M = 20           # a piece is checked every 20 m
 
 
def cell_of(lat, lon):
    """Grid position (row, col) of the tracks.csv cell that contains the point."""
    return (round(lat / CELL_LAT), round(lon / CELL_LON))
 
 
# Cells the sensor bikes rode through often
RIDDEN = {cell_of(lat, lon) for lat, lon, n in TRACKS_ALL[["lat", "lon", "n"]].itertuples(index=False)
          if n >= MIN_RIDES}
 
 
def is_ridden(lat, lon):
    """True if the point lies in a cell the bikes rode often."""
    return cell_of(lat, lon) in RIDDEN
 
 
def ridden_share(line):
    """Part of the piece (0 to 1) that lies on ridden cells, checked every SAMPLE_M meters."""
    samples = []
    # walk along each straight part between two points and take a sample every SAMPLE_M meters
    for p, q in zip(line, line[1:]):
        steps = max(1, int(distance_m(*p, *q) // SAMPLE_M))
        for i in range(steps):
            f = i / steps
            samples.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))
    samples.append(tuple(line[-1]))
    return sum(is_ridden(*s) for s in samples) / len(samples)
# All pieces of all bumpy roads, so a bike street piece that is also a bumpy road can be left out
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
