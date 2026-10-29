"""The time period chosen in the sidebar: all months together, or one month like "2026-06".

These helpers give the areas, tracks, totals and a readable name for a period.
"""
import pandas as pd
from tabs.real_data import AREAS, MONTHS, TRACKS, TRACKS_ALL, DATA_INFO
import tabs.livability  # noqa: F401  (adds the livability score columns to AREAS and MONTHS)
from tabs.translation import t, month_name

ALL_MONTHS = "all"
PERIODS = [ALL_MONTHS] + DATA_INFO["months"]  # the choices in the sidebar


def short_date(day, with_year=False):
    """'2026-06-11' -> '11 Jun' (or '11. Jun' in German), with_year -> '11 Jun 2026'."""
    day = pd.Timestamp(day)
    text = t("short_date", d=day.day, m=month_name(day.month, short=True))
    return f"{text} {day.year}" if with_year else text


def month_short(month):
    """'2026-06' -> 'Jun 26' (column names in the dashboard)."""
    first = pd.Timestamp(month + "-01")
    return f"{month_name(first.month, short=True)} {first:%y}"


def period_label(period):
    """'all' -> 'All months (17 Dec – 19 Oct 2026)', '2026-06' -> 'June 2026 (11–30 Jun)'."""
    if period == ALL_MONTHS:
        return t("period_all", first=short_date(DATA_INFO["first_day"]),
                 last=short_date(DATA_INFO["last_day"], with_year=True))
    totals = DATA_INFO["month_totals"][period]
    first = pd.Timestamp(totals["first_day"])
    if totals["first_day"] == totals["last_day"]:  # only one riding day: 'March 2026 (13 Mar)'
        return t("period_one_day", month=month_name(first.month), year=first.year, day=short_date(first))
    return t("period_month", month=month_name(first.month), year=first.year,
             first=first.day, last=short_date(totals["last_day"]))


def totals_for(period):
    """Readings, sensors, first_day and last_day of the period."""
    if period == ALL_MONTHS:
        # DATA_INFO calls the number of readings "points"; a month calls it "readings"
        return {**DATA_INFO, "readings": DATA_INFO["points"]}
    return DATA_INFO["month_totals"][period]


def areas_for(period):
    """All areas with their results for the period; enough_data=False where a month lacks data."""
    if period == ALL_MONTHS:
        return AREAS.assign(enough_data=True)
    month = MONTHS[MONTHS["month"] == period]
    # start from every area center, so areas without data that month still show (grey on the map)
    centers = AREAS[["area", "label", "lat", "lon"]]
    table = centers.merge(month.drop(columns=["label", "lat", "lon"]), on="area", how="left")
    table["enough_data"] = table["enough_data"].eq(True)  # areas without a row that month -> False
    table[["readings", "days", "riders"]] = table[["readings", "days", "riders"]].fillna(0).astype(int)
    return table


def tracks_for(period):
    """Track cells of one month, or of all months added up."""
    if period == ALL_MONTHS:
        return TRACKS_ALL
    return TRACKS[TRACKS["month"] == period]
