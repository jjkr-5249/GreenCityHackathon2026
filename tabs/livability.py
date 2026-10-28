"""Livability score (0-100) for every measured area, from the real data.

    Livability = w_air * S_air + w_heat * S_heat + w_bike * S_bike

Each part is a score from 0 (bad) to 100 (good). Change WEIGHTS to give a part
more or less say; they are scaled to add up to 1, so any numbers work.
To add a part later (e.g. amenities): compute a "score_<part>" column and add it to WEIGHTS.
"""
from tabs.real_data import AREAS, BIKE_STREETS, BUMPY_ROADS, AREA_RADIUS_M, distance_m
from tabs.routing import route_from_area_to_nearest_bike_street

WEIGHTS = {"air": 0.4, "heat": 0.4, "bike": 0.2}

PM25_WORST = 10.0        # µg/m³ average PM2.5 that scores 0 (twice the WHO yearly guideline of 5)
HEAT_RANGE = 0.5         # °C vs. city at the same hour: -0.5 scores 100, +0.5 scores 0
BIKE_MAX_KM = 5.0        # smooth route to the nearest bike lane street this long or longer scores 0
BUMPY_PENALTY_POINTS = 20  # points off the bike score if a bumpy road is in the area


def clip(x):
    """Keep a score between 0 and 100."""
    return max(0.0, min(100.0, x))


def in_area(area, street):
    """True if any part of the street is inside the area's circle."""
    return any(distance_m(area["lat"], area["lon"], p[0], p[1]) <= AREA_RADIUS_M for p in street["points"])


def air_score(area):
    """Less fine dust -> higher score."""
    return clip(100 * (1 - area["pm25_mean"] / PM25_WORST))


def heat_score(area):
    """Cooler than the city at the same hour -> higher score (less heat island)."""
    return clip(100 * (HEAT_RANGE - area["temp_anom"]) / (2 * HEAT_RANGE))


def bike_score(area):
    """Bike lane street in the area -> 100, else less the further the nearest one is."""
    if any(in_area(area, s) for s in BIKE_STREETS):
        score = 100.0
    else:
        route = route_from_area_to_nearest_bike_street(area["lat"], area["lon"], AREA_RADIUS_M)
        km = route["length_m"] / 1000 if route else BIKE_MAX_KM
        score = 100 * (1 - km / BIKE_MAX_KM)
    if any(in_area(area, r) for r in BUMPY_ROADS if r["points"]):
        score -= BUMPY_PENALTY_POINTS
    return clip(score)


# ─── Add the scores to the areas table ───
AREAS["score_air"] = AREAS.apply(air_score, axis=1)
AREAS["score_heat"] = AREAS.apply(heat_score, axis=1)
AREAS["score_bike"] = AREAS.apply(bike_score, axis=1)
total_weight = sum(WEIGHTS.values())
AREAS["livability"] = sum(AREAS[f"score_{part}"] * w for part, w in WEIGHTS.items()) / total_weight


def mix(color_a, color_b, t):
    """Color between color_a (t=0) and color_b (t=1), both like "#rrggbb"."""
    a = [int(color_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(color_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def livability_color(score):
    """Above 60: light to dark green. 50-60: white. Below 50: light red (49) to strong red (45 and below)."""
    score = round(score)  # same whole number as shown in the popup
    if score > 60:
        return mix("#a5d6a7", "#1b5e20", (score - 60) / 40)  # 61 light green ... 100 dark green
    if score >= 50:
        return "#ffffff"
    redness = min(1, (49 - score) / 4)                      # 49 -> 0, 45 or lower -> 1
    return mix("#ef9a9a", "#b71c1c", redness)                # 49 light red ... 45 strong red
