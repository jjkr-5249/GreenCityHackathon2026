"""📊 Dashboard tab: the area ranking, where Heilbronn needs help, month by month,
and where the sensor bikes measured.

This is the planners' view: it turns the measured data into the places that most need
shade, trees, cleaner air or road repairs.
"""
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
from tabs.real_data import AREAS, MONTHS, BUMPY_ROADS, DATA_INFO, AREA_RADIUS_M, MARKTPLATZ, weighted_mean
from tabs.livability import WEIGHTS, livability_color
from tabs.periods import ALL_MONTHS, period_label, short_date, month_short, tracks_for
from tabs.map_tab import tracks_heatmap
from tabs.translation import t


def grid_color(value):
    """Cell style of the livability-per-month table: the map's color, grey for "–"."""
    if pd.isna(value):
        return "background-color: #eeeeee; color: #9e9e9e"
    text = "white" if round(value) >= 85 or round(value) <= 46 else "#111"  # readable on dark shades
    return f"background-color: {livability_color(value)}; color: {text}"


def render_months():
    """City averages per month, livability of every area in every month, and one area over the months."""
    st.subheader(t("by_month_header"))
    st.caption(t("by_month_caption", readings=DATA_INFO["min_month_readings"], days=DATA_INFO["min_month_days"]))
    months = DATA_INFO["months"]
    names = {m: month_short(m) for m in months}
    ok_months = MONTHS[MONTHS["enough_data"]]

    # City averages per month
    city = pd.DataFrame([{
        "month": names[m],
        "temp_mean": weighted_mean(ok_months[ok_months["month"] == m], "temp_mean"),
        "pm25_mean": weighted_mean(ok_months[ok_months["month"] == m], "pm25_mean"),
    } for m in months])
    labels = {"month": t("month"), "temp_mean": t("col_temp_avg"), "pm25_mean": t("col_pm_avg")}
    col_t, col_p = st.columns(2)
    with col_t:
        fig = px.line(city, x="month", y="temp_mean", markers=True, title=t("chart_city_temp"), labels=labels)
        fig.update_layout(height=280)
        st.plotly_chart(fig, width="stretch")
    with col_p:
        fig = px.line(city, x="month", y="pm25_mean", markers=True, title=t("chart_city_pm"), labels=labels)
        fig.update_traces(line_color="#fb8c00")
        fig.update_layout(height=280)
        st.plotly_chart(fig, width="stretch")

    # Livability of every area in every month, colored like the map
    grid = (ok_months.pivot(index="area", columns="month", values="livability")
            .reindex(columns=months)  # months without any data stay as "–" columns
            .rename(columns=names))
    # first column: all months together; rows sorted from most to least livable
    grid.insert(0, t("all_months_col"), AREAS.set_index("area")["livability"])
    grid = grid.reindex(AREAS.sort_values("livability", ascending=False)["area"])
    st.markdown(t("livability_per_month"))
    st.dataframe(grid.style.map(grid_color).format("{:.0f}", na_rep="–"), width="stretch",
                 height=35 * (len(grid) + 1) + 3)  # tall enough to show every row without scrolling

    # One area over the months
    st.markdown(t("one_area"))
    pick = st.selectbox(t("area"), AREAS.sort_values("label")["area"], key="month_area")
    one = ok_months[ok_months["area"] == pick].sort_values("month")
    if one.empty:
        st.info(t("no_month_data", area=pick))
    else:
        one = one.assign(month=one["month"].map(names))
        col_a, col_b = st.columns(2)
        with col_a:
            fig = px.bar(one, x="month", y="temp_anom", title=t("chart_area_temp", area=pick),
                         labels={"month": t("month"), "temp_anom": t("axis_temp_vs_city")},
                         color="temp_anom", color_continuous_scale="RdBu_r", color_continuous_midpoint=0)
            fig.update_layout(height=280, coloraxis_showscale=False)
            st.plotly_chart(fig, width="stretch")
        with col_b:
            fig = px.bar(one, x="month", y="livability", title=t("chart_area_livability", area=pick),
                         labels={"month": t("month"), "livability": t("axis_livability")}, range_y=[0, 100])
            fig.update_traces(marker_color=[livability_color(v) for v in one["livability"]],
                              marker_line_color="#757575", marker_line_width=1)
            fig.update_layout(height=280)
            st.plotly_chart(fig, width="stretch")
        st.dataframe(one[["month", "livability", "temp_mean", "temp_anom", "pm25_mean", "pm25_anom", "readings", "days"]],
                     column_config={
                         "month": t("month"),
                         "livability": st.column_config.NumberColumn(t("livability"), format="%.0f"),
                         "temp_mean": st.column_config.NumberColumn(t("col_temp_avg"), format="%.1f"),
                         "temp_anom": st.column_config.NumberColumn(t("col_temp_diff"), format="%+.2f"),
                         "pm25_mean": st.column_config.NumberColumn(t("col_pm_avg"), format="%.1f"),
                         "pm25_anom": st.column_config.NumberColumn(t("col_pm_diff"), format="%+.2f"),
                         "readings": t("readings"), "days": t("col_days")},
                     hide_index=True, width="stretch")
    last = DATA_INFO["month_totals"][months[-1]]
    st.caption(t("last_month_note", day=short_date(last["last_day"])))


# ═══ TAB: DASHBOARD ═══
def render():
    st.header(t("dashboard_header"))
    st.caption(t("dashboard_caption", sensors=DATA_INFO["sensors"], points=f"{DATA_INFO['points']:,}",
                 first=short_date(DATA_INFO["first_day"], with_year=True),
                 last=short_date(DATA_INFO["last_day"], with_year=True)))

    # Key numbers
    st.subheader(t("overall_result", period=period_label(ALL_MONTHS)))
    # rank 1 = coolest; the last air rank = most fine dust
    coolest = AREAS[AREAS["rank_temp"] == 1].iloc[0]
    dirtiest = AREAS[AREAS["rank_air"] == len(AREAS)].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("areas_ranked"), len(AREAS))
    c2.metric(t("sensor_bikes"), DATA_INFO["sensors"])
    c3.metric(t("coolest_area"), coolest["label"], t("temp_vs_city", v=coolest["temp_anom"]), delta_color="inverse")
    c4.metric(t("most_dust"), dirtiest["label"], t("pm_vs_city", v=dirtiest["pm25_anom"]), delta_color="inverse")

    st.divider()

    # Temperature and fine dust compared with the whole city at the same hour
    col_temp, col_pm = st.columns(2)

    with col_temp:
        fig1 = px.bar(AREAS.sort_values("temp_anom"), x="label", y="temp_anom",
                      color="temp_anom", color_continuous_scale="RdBu_r", color_continuous_midpoint=0,
                      title=t("chart_temp_vs_city"),
                      labels={"temp_anom": "°C", "label": t("area")})
        fig1.update_layout(height=350, xaxis_tickangle=-45, coloraxis_showscale=False)
        st.plotly_chart(fig1, width="stretch")

    with col_pm:
        fig2 = px.bar(AREAS.sort_values("pm25_anom"), x="label", y="pm25_anom",
                      color="pm25_anom", color_continuous_scale=["#43a047", "#fb8c00", "#e53935"],
                      title=t("chart_pm_vs_city"),
                      labels={"pm25_anom": "µg/m³", "label": t("area")})
        fig2.update_layout(height=350, xaxis_tickangle=-45, coloraxis_showscale=False)
        st.plotly_chart(fig2, width="stretch")

    st.caption(t("gaps_tendency"))

    st.divider()

    # Full ranking, with how the livability score is made (weights from livability.py)
    st.subheader(t("ranking_header"))
    st.caption(t("ranking_caption"))
    total_w = sum(WEIGHTS.values())
    parts = " + ".join(f"{w / total_w:.0%} {t('part_' + part)}" for part, w in WEIGHTS.items())
    st.caption(t("livability_formula", parts=parts))
    st.dataframe(
        AREAS[["rank_overall", "area", "livability", "temp_anom", "temp_mean", "pm25_anom", "pm25_mean", "readings", "days"]],
        column_config={
            "rank_overall": t("col_rank"),
            "area": t("area"),
            "livability": st.column_config.ProgressColumn(t("livability"), min_value=0, max_value=100, format="%.0f"),
            "temp_anom": st.column_config.NumberColumn(t("col_temp_diff"), format="%+.2f"),
            "temp_mean": st.column_config.NumberColumn(t("col_temp_avg"), format="%.1f"),
            "pm25_anom": st.column_config.NumberColumn(t("col_pm_diff"), format="%+.2f"),
            "pm25_mean": st.column_config.NumberColumn(t("col_pm_avg"), format="%.1f"),
            "readings": t("readings"),
            "days": t("col_days"),
        },
        hide_index=True, width="stretch",
    )

    st.divider()

    # Where action would help most
    st.subheader(t("needs_help"))
    col_hot, col_dust, col_roads = st.columns(3)

    with col_hot:
        st.markdown(t("help_warmest"))
        for _, a in AREAS.sort_values("temp_anom", ascending=False).head(5).iterrows():
            st.write(f"🔴 **{a['label']}** — {t('temp_vs_city', v=a['temp_anom'])}")

    with col_dust:
        st.markdown(t("help_dust"))
        for _, a in AREAS.sort_values("pm25_anom", ascending=False).head(5).iterrows():
            st.write(f"🟠 **{a['label']}** — {t('pm_vs_city', v=a['pm25_anom'])}")

    with col_roads:
        st.markdown(t("help_bumpy"))
        for r in sorted(BUMPY_ROADS, key=lambda r: r["avg_rough"], reverse=True)[:5]:
            st.write(f"⚫ **{r['name']}** — {t('roughness', v=r['avg_rough'])}")

    st.divider()

    render_months()

    st.divider()

    # Where the bikes measured: purple tracks heatmap + one circle per ranked area
    st.subheader(t("where_measured"))
    st.write(t("where_measured_intro"))

    cov_map = folium.Map(location=MARKTPLATZ, zoom_start=12, tiles="OpenStreetMap")
    tracks_heatmap(tracks_for(ALL_MONTHS)).add_to(cov_map)
    for _, a in AREAS.iterrows():
        folium.Circle(
            [a["lat"], a["lon"]], radius=AREA_RADIUS_M,
            color="#2e7d32", weight=2, fill=True, fill_opacity=0.1,
            tooltip=t("coverage_tooltip", area=a["area"], readings=f"{a['readings']:,}", days=a["days"])
        ).add_to(cov_map)
    st_folium(cov_map, height=450, use_container_width=True, key="coverage_map")
