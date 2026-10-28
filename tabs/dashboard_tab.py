"""📊 Dashboard tab: the area ranking, where Heilbronn needs help, and where the sensor bikes measured.

This is the planners' view: it turns the measured data into the places that most need
shade, trees, cleaner air or road repairs.
"""
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
from tabs.real_data import AREAS, BUMPY_ROADS, DATA_INFO, AREA_RADIUS_M, MARKTPLATZ
from tabs.livability import WEIGHTS
from tabs.map_tab import tracks_heatmap
from tabs.translation import t


# ═══ TAB: DASHBOARD ═══
def render():
    st.header(t("dashboard_header"))
    st.caption(t("dashboard_caption", sensors=DATA_INFO["sensors"], points=f"{DATA_INFO['points']:,}",
                 first=DATA_INFO["first_day"], last=DATA_INFO["last_day"]))

    # Key numbers
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

    # Where the bikes measured: purple tracks heatmap + one circle per ranked area
    st.subheader(t("where_measured"))
    st.write(t("where_measured_intro"))

    cov_map = folium.Map(location=MARKTPLATZ, zoom_start=12, tiles="OpenStreetMap")
    tracks_heatmap().add_to(cov_map)
    for _, a in AREAS.iterrows():
        folium.Circle(
            [a["lat"], a["lon"]], radius=AREA_RADIUS_M,
            color="#2e7d32", weight=2, fill=True, fill_opacity=0.1,
            tooltip=t("coverage_tooltip", area=a["area"], readings=f"{a['readings']:,}", days=a["days"])
        ).add_to(cov_map)
    st_folium(cov_map, height=450, use_container_width=True, key="coverage_map")
