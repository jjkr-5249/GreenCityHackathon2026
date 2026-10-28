from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent

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

# Where the sensor bikes rode: GPS points grouped into cells of about 55 m
#   lat, lon   center of the cell
#   n          number of readings in the cell
TRACKS = pd.read_csv(DATA_DIR / "tracks.csv")

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
