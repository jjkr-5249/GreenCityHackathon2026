"""Turn the raw openSenseMap bike readings into the tables the app uses.

Run with:  make data   (all files are in the csv/ folder)
Reads:     osem_bike_data.csv  (raw readings),  area_centers.csv  (fixed area positions)
Writes:    heilbronn_area_ranking.csv  one row per area, all months from START_DATE together
           area_months.csv             one row per area and month
           tracks.csv                  where the bikes rode, per month (cells of about 55 m)
           data_info.json              the rules and totals, shown in the app

Rules (also in EcoCity_HN_Method.pdf):
  1. Keep readings from START_DATE onwards that have temperature, PM2.5 and a position.
  2. Drop humid readings (humidity above MAX_HUMIDITY): fine dust sensors read too high in humid air.
  3. Drop PM2.5 above MAX_PM25: impossible outdoors, sensor faults.
  4. Each reading belongs to the nearest area center, if it is at most MAX_KM away.
  5. Same-hour difference: reading minus the median of ALL readings in that same hour (date + hour).
  6. An area needs MIN_READINGS and MIN_DAYS overall; a month needs MIN_MONTH_READINGS and MIN_MONTH_DAYS.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

DIR = Path(__file__).resolve().parent / "csv"
START_DATE = "2025-12-01"   # all data (the first reading is on 14 Dec 2025)
MAX_HUMIDITY = 85           # %
MAX_PM25 = 100              # µg/m³
MAX_KM = 2.5
MIN_READINGS, MIN_DAYS = 300, 3                 # for the overall result
MIN_MONTH_READINGS, MIN_MONTH_DAYS = 100, 3     # for one month
CELL_LAT, CELL_LON = 0.0005, 0.00075            # track cells, about 55 m x 55 m (also in tabs/real_data.py)


def load_readings():
    """Steps 1-4: clean the raw readings and give each one its area."""
    cols = {"boxId": "bike", "createdAt": "time", "latitude": "lat", "longitude": "lon",
            "Temperature": "temp", "Rel. Humidity": "humidity", "Finedust PM2.5": "pm25", "Finedust PM10": "pm10"}
    raw = pd.read_csv(DIR / "osem_bike_data.csv", usecols=list(cols)).rename(columns=cols)
    raw["time"] = pd.to_datetime(raw["time"], format="ISO8601")
    counts = {"raw_rows": len(raw)}

    d = raw.dropna(subset=["temp", "pm25", "lat", "lon"])
    d = d[d["time"] >= START_DATE]
    counts["with_values_from_start"] = len(d)
    d = d[d["humidity"] <= MAX_HUMIDITY]
    counts["after_humidity_rule"] = len(d)
    d = d[d["pm25"] <= MAX_PM25]
    counts["after_pm25_rule"] = len(d)

    # nearest area center (flat-earth distance is accurate enough at this scale)
    centers = pd.read_csv(DIR / "area_centers.csv")
    km_per_deg_lon = 111.2 * np.cos(np.radians(centers["lat"].mean()))
    dlat = (d["lat"].values[:, None] - centers["lat"].values) * 111.2
    dlon = (d["lon"].values[:, None] - centers["lon"].values) * km_per_deg_lon
    dist = np.sqrt(dlat ** 2 + dlon ** 2)
    d = d.assign(area=centers["area"].values[dist.argmin(axis=1)], km=dist.min(axis=1))

    # step 5 uses all clean readings of the city, also those outside the areas
    d["hour"] = d["time"].dt.floor("h")
    d["temp_anom"] = d["temp"] - d.groupby("hour")["temp"].transform("median")
    d["pm25_anom"] = d["pm25"] - d.groupby("hour")["pm25"].transform("median")

    d = d[d["km"] <= MAX_KM].copy()
    counts["in_areas"] = len(d)
    d["day"] = d["time"].dt.date
    d["month"] = d["time"].dt.to_period("M").astype(str)  # like "2026-06"
    return d, centers, counts


def day_se(group, column):
    """Standard error across riding days: every day counts once, however many readings it has."""
    per_day = group.groupby("day")[column].mean()
    return per_day.std(ddof=1) / np.sqrt(len(per_day)) if len(per_day) > 1 else np.nan


def summarize(readings):
    """One row of results for a group of readings (an area, or an area in one month)."""
    return pd.Series({
        "temp_anom": readings["temp_anom"].mean(),
        "temp_anom_se": day_se(readings, "temp_anom"),
        "pm25_anom": readings["pm25_anom"].mean(),
        "pm25_anom_se": day_se(readings, "pm25_anom"),
        "temp_mean": readings["temp"].mean(),
        "pm25_mean": readings["pm25"].mean(),
        "pm10_mean": readings["pm10"].mean(),
        "readings": len(readings),
        "days": readings["day"].nunique(),
        "riders": readings["bike"].nunique(),
        "first": readings["time"].min().strftime("%Y-%m-%d"),
        "last": readings["time"].max().strftime("%Y-%m-%d"),
    })


def add_ranks(table):
    """Ranks among the given areas: 1 = coolest / cleanest. Overall = average of the two z-scores."""
    table = table.copy()
    table["rank_temp"] = table["temp_anom"].rank(method="min").astype(int)
    table["rank_air"] = table["pm25_anom"].rank(method="min").astype(int)
    z = lambda s: (s - s.mean()) / s.std(ddof=0)
    table["score"] = (z(table["temp_anom"]) + z(table["pm25_anom"])) / 2
    table["rank_overall"] = table["score"].rank(method="min").astype(int)
    return table


def main():
    d, centers, counts = load_readings()
    print(f"{counts['raw_rows']:,} raw rows -> {counts['in_areas']:,} clean readings in areas")

    # overall result, all months together
    overall = d.groupby("area").apply(summarize, include_groups=False).reset_index()
    overall = overall[(overall["readings"] >= MIN_READINGS) & (overall["days"] >= MIN_DAYS)]
    overall = add_ranks(overall).merge(centers, on="area").sort_values("rank_overall")
    overall.round(4).to_csv(DIR / "heilbronn_area_ranking.csv", index=False)
    print(f"overall: {len(overall)} areas")

    # result per area and month; ranks only among areas with enough data that month
    months = d.groupby(["area", "month"]).apply(summarize, include_groups=False).reset_index()
    months["enough_data"] = (months["readings"] >= MIN_MONTH_READINGS) & (months["days"] >= MIN_MONTH_DAYS)
    ranked = [add_ranks(g[g["enough_data"]]) for _, g in months.groupby("month")]
    months = months.merge(pd.concat(ranked)[["area", "month", "rank_temp", "rank_air", "score", "rank_overall"]],
                          on=["area", "month"], how="left").merge(centers, on="area")
    months.round(4).to_csv(DIR / "area_months.csv", index=False)
    print(f"months: {months['enough_data'].sum()} of {len(months)} area-months have enough data")

    # where the bikes rode, per month
    cells = d.assign(lat=(d["lat"] / CELL_LAT).round() * CELL_LAT, lon=(d["lon"] / CELL_LON).round() * CELL_LON)
    tracks = cells.groupby(["month", "lat", "lon"]).size().rename("n").reset_index()
    tracks.round(5).to_csv(DIR / "tracks.csv", index=False)

    info = {
        "points": int(counts["in_areas"]), "raw_rows": int(counts["raw_rows"]),
        "sensors": int(d["bike"].nunique()),
        "first_day": d["time"].min().strftime("%Y-%m-%d"), "last_day": d["time"].max().strftime("%Y-%m-%d"),
        "start_date": START_DATE, "max_humidity": MAX_HUMIDITY, "max_pm25": MAX_PM25, "max_km": MAX_KM,
        "min_readings": MIN_READINGS, "min_days": MIN_DAYS,
        "min_month_readings": MIN_MONTH_READINGS, "min_month_days": MIN_MONTH_DAYS,
        "counts": {k: int(v) for k, v in counts.items()},
        "months": sorted(d["month"].unique()),
        "month_totals": {m: {"readings": int(len(g)), "sensors": int(g["bike"].nunique()),
                             "days": int(g["day"].nunique()),
                             "first_day": g["time"].min().strftime("%Y-%m-%d"),
                             "last_day": g["time"].max().strftime("%Y-%m-%d")}
                         for m, g in d.groupby("month")},
    }
    (DIR / "data_info.json").write_text(json.dumps(info, indent=1))
    print("written: heilbronn_area_ranking.csv, area_months.csv, tracks.csv, data_info.json")


if __name__ == "__main__":
    main()
