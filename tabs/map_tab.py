import streamlit as st
import folium
from streamlit_folium import st_folium
from dummy_data import SENSORS, DRINKING_WATER, COOL_SPOTS
from translation import t, opt, get_lang, COOL_SPOTS_DE


# ═══ TAB 1: MAP ═══
def render(season, show_temp, show_water, show_cool, show_air):
    lang = get_lang()
    if "selected_spot" not in st.session_state:
        st.session_state.selected_spot = None

    st.header(t("map_header_summer") if not season else t("map_header_winter"))

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("avg_temp"), f"{SENSORS['temperature'].mean():.1f}°C")
    c2.metric(t("avg_humidity"), f"{SENSORS['humidity'].mean():.0f}%")
    c3.metric(t("avg_pm25"), f"{SENSORS['pm25'].mean():.1f} µg/m³")
    c4.metric(t("comfort"), f"{SENSORS['comfort'].mean():.0f}/100")

    # Layout: spots list on left, map on right
    col_spots, col_map = st.columns([1, 3])

    sorted_s = SENSORS.sort_values("temperature")

    with col_spots:
        st.subheader(t("hottest"))
        for _, r in sorted_s.tail(5).iloc[::-1].iterrows():
            if st.button(f"🔴 {r['name']} — {r['temperature']}°C", key=f"hot_{r['id']}", use_container_width=True):
                st.session_state.selected_spot = r['id']

        st.subheader(t("coolest"))
        for _, r in sorted_s.head(5).iterrows():
            if st.button(f"🔵 {r['name']} — {r['temperature']}°C", key=f"cool_{r['id']}", use_container_width=True):
                st.session_state.selected_spot = r['id']

        if st.session_state.selected_spot:
            if st.button(t("reset_view"), key="reset_view", use_container_width=True):
                st.session_state.selected_spot = None
                st.rerun()

    with col_map:
        # Determine map center and zoom
        selected = st.session_state.selected_spot
        if selected:
            spot_row = SENSORS[SENSORS["id"] == selected].iloc[0]
            map_center = [spot_row["lat"], spot_row["lon"]]
            map_zoom = 16
        else:
            map_center = [49.1427, 9.2109]
            map_zoom = 14

        m = folium.Map(location=map_center, zoom_start=map_zoom, tiles="OpenStreetMap")

        # Temperature heatmap
        if show_temp:
            from folium.plugins import HeatMap
            heat_data = [[r["lat"], r["lon"], r["temperature"]] for _, r in SENSORS.iterrows()]
            HeatMap(heat_data, radius=40, blur=30).add_to(m)

        # Highlight selected spot
        if selected:
            spot_row = SENSORS[SENSORS["id"] == selected].iloc[0]
            folium.Circle(
                [spot_row["lat"], spot_row["lon"]],
                radius=200,
                color="#ffd600",
                fill=True,
                fill_color="#ffd600",
                fill_opacity=0.25,
                weight=3,
                tooltip=t("selected", name=spot_row['name'])
            ).add_to(m)

        # Sensor markers
        for _, r in SENSORS.iterrows():
            is_selected = (selected == r["id"])
            color = "blue" if r["temperature"] < 29 else "orange" if r["temperature"] < 33 else "red"

            popup = f"""<b>{r['name']}</b><br>
            🌡️ {r['temperature']}°C<br>
            💧 {r['humidity']}%<br>
            🌬️ PM2.5: {r['pm25']} µg/m³<br>
            PM10: {r['pm10']} µg/m³<br>
            ⭐ {t('comfort')}: {r['comfort']}/100"""

            if is_selected:
                icon = folium.Icon(color="cadetblue", icon="star", prefix="fa")
            else:
                icon = folium.Icon(color=color, icon="thermometer-half", prefix="fa")

            folium.Marker(
                [r["lat"], r["lon"]],
                popup=popup,
                tooltip=f"{r['name']}: {r['temperature']}°C",
                icon=icon
            ).add_to(m)

        # Water spots
        if show_water:
            for w in DRINKING_WATER:
                color = "blue" if w["status"] == "working" else "red" if w["status"] == "broken" else "gray"
                status = "✅" if w["status"] == "working" else "❌" if w["status"] == "broken" else "⚠️"
                folium.Marker(
                    [w["lat"], w["lon"]],
                    popup=f"💧 {w['name']}<br>Status: {status} {opt(w['status'])}",
                    tooltip=f"💧 {w['name']} ({status})",
                    icon=folium.Icon(color=color, icon="tint", prefix="fa")
                ).add_to(m)

        # Cool spots
        if show_cool:
            for s in COOL_SPOTS:
                desc = COOL_SPOTS_DE.get(s["name"], s["desc"]) if lang == "de" else s["desc"]
                folium.Marker(
                    [s["lat"], s["lon"]],
                    popup=f"🌳 {s['name']}<br>{desc}",
                    tooltip=f"🌳 {s['name']}",
                    icon=folium.Icon(color="green", icon="tree", prefix="fa")
                ).add_to(m)

        # Air quality circles
        if show_air:
            for _, r in SENSORS.iterrows():
                color = "#4caf50" if r["pm25"] < 12 else "#ff9800" if r["pm25"] < 25 else "#f44336"
                folium.Circle(
                    [r["lat"], r["lon"]], radius=150,
                    color=color, fill=True, fill_opacity=0.3,
                    tooltip=f"PM2.5: {r['pm25']} µg/m³"
                ).add_to(m)

        st_folium(m, height=550, use_container_width=True)

        # Show selected spot details
        if selected:
            spot_row = SENSORS[SENSORS["id"] == selected].iloc[0]
            st.info(f"📍 **{spot_row['name']}** — {spot_row['temperature']}°C | {t('humidity')}: {spot_row['humidity']}% | PM2.5: {spot_row['pm25']} µg/m³ | {t('comfort')}: {spot_row['comfort']}/100")
