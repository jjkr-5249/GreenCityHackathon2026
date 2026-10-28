import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
from dummy_data import SENSORS, HOURLY_TEMPS, HOURLY_PM
from translation import t, opt, get_lang, translate_sensor_type


# ═══ TAB 4: DASHBOARD ═══
def render():
    lang = get_lang()

    st.header(t("dashboard_header"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("sensors"), "15")
    c2.metric(t("hot_days"), "12")
    c3.metric(t("coolest_spot"), "Waldgebiet (26.2°C)")
    c4.metric(t("worst_air"), "Industrie (28.4 µg/m³)")

    st.divider()

    # Temperature chart
    fig1 = px.line(HOURLY_TEMPS.assign(type=HOURLY_TEMPS["type"].map(opt)), x="hour", y="temperature", color="type",
                   title=t("chart_daily_temp"),
                   labels={"temperature": "°C", "hour": t("hour"), "type": t("area_type")})
    fig1.update_layout(height=350)
    st.plotly_chart(fig1, use_container_width=True)

    # PM chart
    col_pm, col_bar = st.columns(2)

    with col_pm:
        fig2 = px.line(HOURLY_PM.assign(type=HOURLY_PM["type"].map(opt)), x="hour", y="pm25", color="type",
                       title=t("chart_pm"),
                       labels={"pm25": "µg/m³", "hour": t("hour"), "type": t("area_type")})
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)

    with col_bar:
        fig3 = px.bar(SENSORS.sort_values("temperature"), x="name", y="temperature",
                      color="temperature", color_continuous_scale=["#2196f3", "#ff9800", "#f44336"],
                      title=t("chart_temp_location"),
                      labels={"name": t("location"), "temperature": "°C"})
        fig3.update_layout(height=300, xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # Gap analysis
    st.subheader(t("needs_help"))

    col_gaps, col_recs = st.columns(2)

    with col_gaps:
        st.markdown(t("hottest_least_infra"))
        hot = SENSORS[SENSORS["temperature"] > 33].sort_values("temperature", ascending=False)
        for _, r in hot.iterrows():
            st.write(f"🔴 **{r['name']}** — {r['temperature']}°C, {t('comfort')} {r['comfort']}/100")

    with col_recs:
        st.markdown(t("recommendations"))
        recs = [
            t("rec_trees_industrie"),
            t("rec_fountain_kaiser"),
            t("rec_shade_bahnhof"),
            t("rec_fix_pfuehl"),
            t("rec_canopy_markt"),
        ]
        for r in recs:
            st.write(r)

    st.divider()

    # Sensor coverage map
    st.subheader(t("coverage_header"))
    st.write(t("coverage_intro"))

    cov_map = folium.Map(location=[49.1427, 9.2109], zoom_start=14, tiles="OpenStreetMap")

    for _, loc in SENSORS.iterrows():
        # Coverage circle
        folium.Circle(
            [loc["lat"], loc["lon"]],
            radius=300,
            color="#4caf50",
            fill=True,
            fill_opacity=0.15,
            tooltip=f"{loc['name']} — {translate_sensor_type(loc['type'], lang)}"
        ).add_to(cov_map)

        # Sensor marker
        folium.Marker(
            [loc["lat"], loc["lon"]],
            tooltip=f"📡 {loc['name']}",
            icon=folium.Icon(color="green", icon="signal", prefix="fa")
        ).add_to(cov_map)

    # Mark areas with NO coverage as red zones
    gap_zones = [
        {"name": "Horkheim", "lat": 49.1250, "lon": 9.2000, "reason": t("gap_residential")},
        {"name": "Frankenbach", "lat": 49.1650, "lon": 9.2100, "reason": t("gap_suburb")},
        {"name": "Klingenberg", "lat": 49.1550, "lon": 9.2350, "reason": t("gap_highway")},
        {"name": "Südstadt", "lat": 49.1330, "lon": 9.2150, "reason": t("gap_dense")},
    ]

    for gap in gap_zones:
        folium.Circle(
            [gap["lat"], gap["lon"]],
            radius=400,
            color="#f44336",
            fill=True,
            fill_opacity=0.2,
            tooltip=f"⚠️ {t('gap')}: {gap['name']} — {gap['reason']}"
        ).add_to(cov_map)

        folium.Marker(
            [gap["lat"], gap["lon"]],
            tooltip=f"⚠️ {gap['name']}: {gap['reason']}",
            icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
        ).add_to(cov_map)

    st_folium(cov_map, height=450, use_container_width=True)

    st.markdown(t("coverage_legend"))
