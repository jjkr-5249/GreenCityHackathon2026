"""🗺️ City Map tab: measured areas, sensor bike tracks, bike streets, smooth routes and bumpy roads.

The map layers are switched on and off in the sidebar (see app.py), which passes them to render().
"""
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import numpy as np
from tabs.real_data import (AREAS, TRACKS, BIKE_STREETS, BUMPY_ON_MAP, DATA_INFO, AREA_RADIUS_M,
                            MIN_RIDES, MARKTPLATZ, weighted_mean)
from tabs.livability import livability_color, in_area
from tabs.routing import route_to_nearest_bike_street, route_from_area_to_nearest_bike_street
from tabs.translation import t

INDENT = "<br>&nbsp;&nbsp;&nbsp;&nbsp;"  # new, indented line in a map popup


def small_bike_icon(color):
    """Small round bike sign, about 1/3 of a normal map marker (14 px instead of 41 px)."""
    html = f"""<div style="transform: translate(-50%, -50%); width: 14px; height: 14px;
        border-radius: 50%; background: {color}; border: 1px solid white;
        display: flex; align-items: center; justify-content: center;">
        <i class="fa-solid fa-bicycle" style="color: white; font-size: 8px;"></i></div>"""
    return folium.DivIcon(html=html, icon_size=(0, 0))


def tracks_heatmap():
    """Where the sensor bikes rode, as a purple heatmap (also used on the Dashboard)."""
    # log scale, so busy roads don't hide the quiet ones (n goes from 1 to ~8000)
    weight = np.log1p(TRACKS["n"]) / np.log1p(TRACKS["n"].max())
    return HeatMap(list(zip(TRACKS["lat"], TRACKS["lon"], weight)), radius=6, blur=4, min_opacity=0.4,
                   gradient={0.2: "#d1c4e9", 0.6: "#7e57c2", 1.0: "#311b92"})


def lane_kind(street, full=False):
    """'own bike lane' or 'shared with cars' in the page language (full = longer label with icon)."""
    if street["type"] == "lane":
        return t("own_lane_full") if full else t("own_lane")
    return t("shared_lane_full") if full else t("shared_lane")


def fit_to(m, points):
    """Zoom the map so all [lat, lon] points are visible."""
    m.fit_bounds([[min(p[0] for p in points), min(p[1] for p in points)],
                  [max(p[0] for p in points), max(p[1] for p in points)]])


def draw_street(m, street, color, tip, info):
    """A street on the map: a line along each of its pieces, plus a small bike sign in the middle."""
    # each map item needs its own Popup object (folium gives an element only one parent)
    for line in street["lines"]:
        folium.PolyLine(line, color=color, weight=5, opacity=0.85,
                        tooltip=tip, popup=folium.Popup(info, max_width=250)).add_to(m)
    folium.Marker([street["lat"], street["lon"]], popup=folium.Popup(info, max_width=250), tooltip=tip,
                  icon=small_bike_icon(color)).add_to(m)


def area_popup(a):
    """Popup text of a measured area: livability, temperature, air, bike lanes and bumpy roads."""
    air = (t("air_cleaner") if a["pm25_anom"] < 0.1
           else t("air_slightly_worse") if a["pm25_anom"] < 0.4 else t("air_more_dust"))

    # Bike streets with any part inside this area's circle
    bikes = "".join(INDENT + t("bike_in_area", name=b["name"], kind=lane_kind(b), n=b["segments"])
                    for b in BIKE_STREETS if in_area(a, b))
    if not bikes:
        bikes = INDENT + t("no_bike_street")
        # ...but maybe a smooth route leads to one
        link = route_from_area_to_nearest_bike_street(a["lat"], a["lon"], AREA_RADIUS_M)
        if link:
            via = t("via", streets=", ".join(link["streets"][:3])) if link["streets"] else ""
            warn = t("crosses_bumpy") if link["uses_bumpy"] else ""
            bikes += INDENT + t("nearest_link", target=link["target"],
                                km=link["length_m"] / 1000, via=via, warn=warn)

    # Bumpy roads with any part inside this area's circle
    bumps = "".join(INDENT + t("bumpy_in_area", name=r["name"], avg=r["avg_rough"], peak=r["peak_rough"])
                    for r in BUMPY_ON_MAP if in_area(a, r))
    if not bumps:
        bumps = INDENT + t("no_bumpy")

    return f"""<b>📡 {a['area']}</b> · {t('rank_of', rank=a['rank_overall'], total=len(AREAS))}<br><br>
    🏙️ <b>{t('livability')}:</b> {a['livability']:.0f}/100{INDENT}{t('livability_parts', air=a['score_air'], heat=a['score_heat'], bike=a['score_bike'])}<br>
    🌡️ <b>{t('temperature')}:</b> {a['temp_mean']:.1f}°C{INDENT}{t('vs_city_same_hour', anom=a['temp_anom'])}<br>
    🌬️ <b>{t('air_quality')}:</b> {air}{INDENT}PM2.5: {a['pm25_mean']:.1f} µg/m³ ({a['pm25_anom']:+.2f} {t('vs_city')}){INDENT}PM10: {a['pm10_mean']:.1f} µg/m³<br>
    🚲 <b>{t('bike_lanes')}:</b>{bikes}<br>
    🛣️ <b>{t('bumpy_roads')}:</b>{bumps}<br><br>
    <small>{t('area_footer', readings=a['readings'], days=a['days'], riders=a['riders'])}</small>"""


def area_color(a, real_by):
    """Fill color and opacity of an area circle for the "Color areas by" choice in the sidebar."""
    if real_by == "livability":
        # green above 60, white 50-60, light to strong red below 50 (see livability.py)
        return livability_color(a["livability"]), 0.6
    if real_by == "temperature":
        # blue = cooler than the rest of the city at the same hour, orange = warmer
        return "#1565c0" if a["temp_anom"] < -0.2 else "#64b5f6" if a["temp_anom"] < 0 else "#fb8c00", 0.35
    # green = cleaner air, orange/red = more fine dust than the rest of the city
    return "#43a047" if a["pm25_anom"] < 0.1 else "#fb8c00" if a["pm25_anom"] < 0.4 else "#e53935", 0.35


# ═══ TAB: CITY MAP ═══
def render(show_real, real_by, show_tracks, show_bike_streets, show_access, show_bumpy):
    # The selected area (its full name, or None)
    if "selected_spot" not in st.session_state:
        st.session_state.selected_spot = None
    # The bike street clicked on the map (its name, or None), and the last map click we handled
    if "selected_bike" not in st.session_state:
        st.session_state.selected_bike = None
        st.session_state.last_click = None

    st.header(t("map_header"))
    st.caption(t("measured_by", sensors=DATA_INFO["sensors"],
                 first=DATA_INFO["first_day"], last=DATA_INFO["last_day"]))

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("avg_temp"), f"{weighted_mean('temp_mean'):.1f}°C")
    c2.metric(t("avg_pm25"), f"{weighted_mean('pm25_mean'):.1f} µg/m³")
    c3.metric(t("sensor_bikes"), DATA_INFO["sensors"])
    c4.metric(t("readings"), f"{DATA_INFO['points']:,}")

    # Layout: area list on left, map on right
    col_spots, col_map = st.columns([1, 3])

    # Sorted by the difference from the rest of the city at the same hour
    by_temp = AREAS.sort_values("temp_anom")

    with col_spots:
        st.subheader(t("warmest_areas"))
        st.caption(t("vs_city_now"))
        for _, a in by_temp.tail(5).iloc[::-1].iterrows():
            if st.button(f"🔴 {a['label']} {a['temp_anom']:+.2f}°C", key=f"hot_{a['label']}", width="stretch"):
                st.session_state.selected_spot = a["area"]

        st.subheader(t("coolest_areas"))
        for _, a in by_temp.head(5).iterrows():
            if st.button(f"🔵 {a['label']} {a['temp_anom']:+.2f}°C", key=f"cool_{a['label']}", width="stretch"):
                st.session_state.selected_spot = a["area"]

        if show_access:
            st.subheader(t("access_header"))
            st.caption(t("access_caption", n=MIN_RIDES))
            for b in BIKE_STREETS:
                if b["access_lines"]:
                    checked = t("access_checked", km=b["access_km"], total=b["length_km"])
                else:
                    checked = t("access_no_data")
                st.markdown(f"**{b['name']}**  \n{lane_kind(b, full=True)} · {checked}")

        if st.session_state.selected_spot:
            if st.button(t("reset_view"), width="stretch"):
                st.session_state.selected_spot = None
                st.rerun()

    with col_map:
        # Determine map center and zoom
        selected = st.session_state.selected_spot
        selected_row = AREAS[AREAS["area"] == selected].iloc[0] if selected else None
        if selected:
            m = folium.Map(location=[selected_row["lat"], selected_row["lon"]], zoom_start=15, tiles="OpenStreetMap")
        else:
            m = folium.Map(location=MARKTPLATZ, zoom_start=13, tiles="OpenStreetMap")

        # Smooth route from the clicked bike street to the nearest other bike street
        route = None
        if show_bike_streets and st.session_state.selected_bike:
            route = route_to_nearest_bike_street(st.session_state.selected_bike)

        # With a route: zoom to the clicked street, the route and the street it leads to
        if route and not selected:
            ends = [b for b in BIKE_STREETS if b["name"] in (st.session_state.selected_bike, route["target"])]
            fit_to(m, [p for line in route["lines"] for p in line] + [p for b in ends for p in b["points"]])
        # Without a selection, zoom so all measured areas and streets fit
        elif not selected and (show_real or show_bike_streets or show_bumpy):
            points = []
            if show_real:
                points += AREAS[["lat", "lon"]].values.tolist()
            if show_bike_streets:
                points += [p for b in BIKE_STREETS for p in b["points"]]
            if show_bumpy:
                points += [p for r in BUMPY_ON_MAP for p in r["points"]]
            fit_to(m, points)

        if show_tracks:
            tracks_heatmap().add_to(m)

        # Real measured areas (openSenseMap bike sensors)
        if show_real:
            for _, a in AREAS.iterrows():
                color, fill_opacity = area_color(a, real_by)
                # a white circle needs a grey edge to be visible on the map
                edge = "#757575" if color == "#ffffff" else color
                popup = area_popup(a)
                tooltip = t("area_tooltip", area=a["area"])
                folium.Circle(
                    [a["lat"], a["lon"]], radius=AREA_RADIUS_M,
                    color=edge, weight=2, fill=True, fill_color=color, fill_opacity=fill_opacity,
                    tooltip=tooltip, popup=folium.Popup(popup, max_width=280)
                ).add_to(m)

                # Clickable name label in the middle of the circle
                label = f"""<div style="transform: translate(-50%, -50%); width: max-content;
                    background: white; color: #111; border: 2px solid {edge}; border-radius: 10px;
                    padding: 1px 6px; font: bold 11px sans-serif; cursor: pointer;">{a['label']}</div>"""
                folium.Marker(
                    [a["lat"], a["lon"]],
                    icon=folium.DivIcon(html=label, icon_size=(0, 0)),
                    tooltip=tooltip, popup=folium.Popup(popup, max_width=280)
                ).add_to(m)

        # Accessible routes: wide blue band along the checked parts of the bike streets
        # (dark blue = own bike lane, light blue = shared with cars), under the violet street lines
        if show_access:
            for b in BIKE_STREETS:
                if not b["access_lines"]:
                    continue
                info = t("access_popup", name=b["name"], area=b["area"], kind=lane_kind(b, full=True),
                         km=b["access_km"], total=b["length_km"])
                folium.PolyLine(
                    b["access_lines"], color="#0d47a1" if b["type"] == "lane" else "#64b5f6",
                    weight=12, opacity=0.5,
                    tooltip=t("access_tooltip", name=b["name"], kind=lane_kind(b), km=b["access_km"]),
                    popup=folium.Popup(info, max_width=250)
                ).add_to(m)

        # The smooth route: thick green line (drawn under the violet bike streets)
        if route:
            tip = t("route_tooltip", target=route["target"], km=route["length_m"] / 1000)
            for line in route["lines"]:
                folium.PolyLine(line, color="#00c853", weight=9, opacity=0.9, tooltip=tip).add_to(m)

        # Good bike streets: violet line along the real street + violet bike sign
        # (drawn after the area circles, so the lines stay on top and clickable)
        if show_bike_streets:
            for b in BIKE_STREETS:
                info = (f"<b>{b['name']}</b><br>{b['area']}<br><br>{lane_kind(b, full=True)}<br>"
                        f"{t('street_segments', n=b['segments'])}")
                # the tooltip must start with 🚲 and contain the name: map clicks are matched by it
                draw_street(m, b, "#8e24aa", t("bike_tooltip", name=b["name"], n=b["segments"]), info)

        # Bumpy roads: black line along the real street + black bike sign in the middle
        if show_bumpy:
            for r in BUMPY_ON_MAP:
                info = (f"<b>🛣️ {r['name']}</b><br>{t('avg_roughness', v=r['avg_rough'])}<br>"
                        f"{t('peak_roughness', v=r['peak_rough'])}<br>{t('segments_with_data', n=r['segments'])}")
                draw_street(m, r, "black", t("bumpy_tooltip", name=r["name"], v=r["avg_rough"]), info)

        # Highlight the selected area with a yellow ring
        if selected:
            folium.Circle([selected_row["lat"], selected_row["lon"]], radius=AREA_RADIUS_M + 60,
                          color="#ffd600", weight=4, fill=False,
                          tooltip=t("selected", name=selected)).add_to(m)

        # Only clicks send data back, so moving or zooming the map doesn't reload the page
        result = st_folium(m, height=550, use_container_width=True,
                           returned_objects=["last_object_clicked", "last_object_clicked_tooltip"])

        # A new click on a bike street: remember it and redraw the map with its route
        tip = (result or {}).get("last_object_clicked_tooltip") or ""
        click = (tip, str((result or {}).get("last_object_clicked")))
        if click != st.session_state.last_click:
            st.session_state.last_click = click
            clicked = next((b["name"] for b in BIKE_STREETS
                            if tip.startswith("🚲") and b["name"] in tip.replace("&amp;", "&")), None)
            if clicked and clicked != st.session_state.selected_bike:
                st.session_state.selected_bike = clicked
                st.session_state.selected_spot = None
                st.rerun()

        # Explain the route under the map
        if route:
            start = st.session_state.selected_bike
            if route["length_m"] < 50:
                st.success(t("route_direct", start=start, target=route["target"]))
            else:
                via = ", ".join(route["streets"]) or t("small_paths")
                note = t("route_bumpy_note") if route["uses_bumpy"] else t("route_smooth_note")
                st.success(t("route_found", start=start, target=route["target"],
                             km=route["length_m"] / 1000, via=via, note=note))
            if st.button(t("clear_route")):
                st.session_state.selected_bike = None
                st.rerun()
        elif show_bike_streets:
            st.caption(t("click_hint"))

        # Show the selected area's values
        if selected:
            a = selected_row
            st.info(t("area_info", area=a["area"], rank=a["rank_overall"], total=len(AREAS),
                      temp=a["temp_mean"], anom=a["temp_anom"], pm25=a["pm25_mean"], pm10=a["pm10_mean"]))
