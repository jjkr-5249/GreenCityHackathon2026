import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
import numpy as np
from community_examples import MEETUPS, RATINGS
from real_data import (AREAS, TRACKS, BIKE_STREETS, BUMPY_ROADS, DATA_INFO, AREA_RADIUS_M,
                       MIN_RIDES, distance_m)
from livability import WEIGHTS, livability_color
from routing import route_to_nearest_bike_street, route_from_area_to_nearest_bike_street
from translation import t, opt, get_lang, MEETUPS_DE, RATING_COMMENTS_DE

# Only bumpy roads found in the road network can go on the map
BUMPY_ON_MAP = [r for r in BUMPY_ROADS if r["lat"] is not None and r["lon"] is not None]

AREA_NAMES = AREAS["area"].tolist()  # used as locations in the forms
MARKTPLATZ = [49.1422, 9.2190]
INDENT = "<br>&nbsp;&nbsp;&nbsp;&nbsp;"  # new, indented line in a map popup


def weighted_mean(column):
    """Average over all areas, weighted by how many readings each area has."""
    return (AREAS[column] * AREAS["readings"]).sum() / AREAS["readings"].sum()


def small_bike_icon(color):
    """Small round bike sign, about 1/3 of a normal map marker (14 px instead of 41 px)."""
    html = f"""<div style="transform: translate(-50%, -50%); width: 14px; height: 14px;
        border-radius: 50%; background: {color}; border: 1px solid white;
        display: flex; align-items: center; justify-content: center;">
        <i class="fa-solid fa-bicycle" style="color: white; font-size: 8px;"></i></div>"""
    return folium.DivIcon(html=html, icon_size=(0, 0))


def tracks_heatmap():
    """Where the sensor bikes rode, as a purple heatmap."""
    # log scale, so busy roads don't hide the quiet ones (n goes from 1 to ~8000)
    weight = np.log1p(TRACKS["n"]) / np.log1p(TRACKS["n"].max())
    return HeatMap(list(zip(TRACKS["lat"], TRACKS["lon"], weight)), radius=6, blur=4, min_opacity=0.4,
                   gradient={0.2: "#d1c4e9", 0.6: "#7e57c2", 1.0: "#311b92"})


def lane_kind(street, full=False):
    """'own bike lane' or 'shared with cars' in the page language (full = longer label with icon)."""
    if street["type"] == "lane":
        return t("own_lane_full") if full else t("own_lane")
    return t("shared_lane_full") if full else t("shared_lane")


def idea_header(emoji, title, badge, badge_color, meta, background):
    """Colored title bar of an idea on the ideas board."""
    st.markdown(f"""
    <div style="background: {background}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem;">{emoji}</span>
            <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">{title}</span>
            <span style="background: {badge_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">{badge}</span>
        </div>
        <p style="color: #555; font-size: 0.85rem;">{meta}</p>
    </div>
    """, unsafe_allow_html=True)


def idea_buttons(n, votes, comments):
    """Vote, comment and map buttons under an idea."""
    c1, c2, c3 = st.columns(3)
    c1.button(t("n_votes", n=votes), key=f"vote_{n}", width="stretch")
    c2.button(t("n_comments", n=comments), key=f"comment_{n}", width="stretch")
    c3.button(t("show_on_map"), key=f"map_{n}", width="stretch")


# ─── Page config ───
st.set_page_config(page_title="EcoCity HN", page_icon="🌿", layout="wide")

# ─── Language switch, top right ───
st.markdown("""
<style>
.st-key-lang_switch {
    position: fixed;
    top: 1.1rem;
    right: 13.5rem;
    width: auto !important;
    z-index: 999991;
}
</style>
""", unsafe_allow_html=True)
with st.container(key="lang_switch"):
    st.toggle("ENG / DE", key="lang_de", help="English ⇄ Deutsch")

# ─── Sidebar ───
with st.sidebar:
    st.title("🌿 EcoCity HN")
    st.caption(t("tagline"))
    st.divider()

    st.subheader(t("map_layers"))
    show_real = st.checkbox(t("layer_real"), value=True)
    real_by = "livability"
    if show_real:
        real_by = st.radio(t("color_by"), ["livability", "temperature", "pm25"],
                           format_func=lambda key: t(f"color_{key}"))
        if real_by == "livability":
            st.caption(t("livability_legend"))
    show_tracks = st.checkbox(t("layer_tracks"), value=False)
    show_bike_streets = st.checkbox(t("layer_bike_streets"), value=True)
    show_access = st.checkbox(t("layer_access"), value=False)
    show_bumpy = st.checkbox(t("layer_bumpy"), value=True)
    missing = len(BUMPY_ROADS) - len(BUMPY_ON_MAP)
    if show_bumpy and missing:
        st.caption(t("bumpy_missing", missing=missing, total=len(BUMPY_ROADS)))

    st.divider()
    st.caption("Green City Heilbronn Hackathon 2026")

# ─── Tabs ───
tab_map, tab_community, tab_rate, tab_dashboard = st.tabs([
    t("tab_map"), t("tab_community"), t("tab_rate"), t("tab_dashboard"),
])

# ─── Session state for the selected area (its full name, or None) ───
if "selected_spot" not in st.session_state:
    st.session_state.selected_spot = None
# The bike street clicked on the map (its name, or None), and the last map click we handled
if "selected_bike" not in st.session_state:
    st.session_state.selected_bike = None
    st.session_state.last_click = None

# ═══ TAB 1: MAP ═══
with tab_map:
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
            pts = [p for line in route["lines"] for p in line] + [p for b in ends for p in b["points"]]
            m.fit_bounds([[min(p[0] for p in pts), min(p[1] for p in pts)],
                          [max(p[0] for p in pts), max(p[1] for p in pts)]])
        # Without a selection, zoom so all measured areas and streets fit
        elif not selected and (show_real or show_bike_streets or show_bumpy):
            lats, lons = [], []
            if show_real:
                lats += AREAS["lat"].tolist()
                lons += AREAS["lon"].tolist()
            if show_bike_streets:
                lats += [p[0] for b in BIKE_STREETS for p in b["points"]]
                lons += [p[1] for b in BIKE_STREETS for p in b["points"]]
            if show_bumpy:
                lats += [p[0] for r in BUMPY_ON_MAP for p in r["points"]]
                lons += [p[1] for r in BUMPY_ON_MAP for p in r["points"]]
            m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])

        if show_tracks:
            tracks_heatmap().add_to(m)

        # Real measured areas (openSenseMap bike sensors)
        if show_real:
            for _, a in AREAS.iterrows():
                fill_opacity = 0.35
                if real_by == "livability":
                    # green above 60, white 50-60, light to strong red below 50 (see livability.py)
                    color = livability_color(a["livability"])
                    fill_opacity = 0.6
                elif real_by == "temperature":
                    # blue = cooler than the rest of the city at the same hour, orange = warmer
                    color = "#1565c0" if a["temp_anom"] < -0.2 else "#64b5f6" if a["temp_anom"] < 0 else "#fb8c00"
                else:
                    # green = cleaner air, orange/red = more fine dust than the rest of the city
                    color = "#43a047" if a["pm25_anom"] < 0.1 else "#fb8c00" if a["pm25_anom"] < 0.4 else "#e53935"
                # a white circle needs a grey edge to be visible on the map
                edge = "#757575" if color == "#ffffff" else color
                air = (t("air_cleaner") if a["pm25_anom"] < 0.1
                       else t("air_slightly_worse") if a["pm25_anom"] < 0.4 else t("air_more_dust"))

                # Bike streets with any part inside this area's circle
                bikes = ""
                for b in BIKE_STREETS:
                    if any(distance_m(a["lat"], a["lon"], p[0], p[1]) <= AREA_RADIUS_M for p in b["points"]):
                        bikes += INDENT + t("bike_in_area", name=b["name"], kind=lane_kind(b), n=b["segments"])
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
                bumps = ""
                for r in BUMPY_ON_MAP:
                    if any(distance_m(a["lat"], a["lon"], p[0], p[1]) <= AREA_RADIUS_M for p in r["points"]):
                        bumps += INDENT + t("bumpy_in_area", name=r["name"], avg=r["avg_rough"], peak=r["peak_rough"])
                if not bumps:
                    bumps = INDENT + t("no_bumpy")
                popup = f"""<b>📡 {a['area']}</b> · {t('rank_of', rank=a['rank_overall'], total=len(AREAS))}<br><br>
                🏙️ <b>{t('livability')}:</b> {a['livability']:.0f}/100{INDENT}{t('livability_parts', air=a['score_air'], heat=a['score_heat'], bike=a['score_bike'])}<br>
                🌡️ <b>{t('temperature')}:</b> {a['temp_mean']:.1f}°C{INDENT}{t('vs_city_same_hour', anom=a['temp_anom'])}<br>
                🌬️ <b>{t('air_quality')}:</b> {air}{INDENT}PM2.5: {a['pm25_mean']:.1f} µg/m³ ({a['pm25_anom']:+.2f} {t('vs_city')}){INDENT}PM10: {a['pm10_mean']:.1f} µg/m³<br>
                🚲 <b>{t('bike_lanes')}:</b>{bikes}<br>
                🛣️ <b>{t('bumpy_roads')}:</b>{bumps}<br><br>
                <small>{t('area_footer', readings=a['readings'], days=a['days'], riders=a['riders'])}</small>"""
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
                tip = t("bike_tooltip", name=b["name"], n=b["segments"])
                for line in b["lines"]:
                    folium.PolyLine(line, color="#8e24aa", weight=5, opacity=0.85,
                                    tooltip=tip, popup=folium.Popup(info, max_width=250)).add_to(m)
                folium.Marker(
                    [b["lat"], b["lon"]],
                    popup=folium.Popup(info, max_width=250),
                    tooltip=tip,
                    icon=small_bike_icon("#8e24aa")
                ).add_to(m)

        # Bumpy roads: black line along the real street + black bike sign in the middle
        if show_bumpy:
            for r in BUMPY_ON_MAP:
                info = (f"<b>🛣️ {r['name']}</b><br>{t('avg_roughness', v=r['avg_rough'])}<br>"
                        f"{t('peak_roughness', v=r['peak_rough'])}<br>{t('segments_with_data', n=r['segments'])}")
                tip = t("bumpy_tooltip", name=r["name"], v=r["avg_rough"])
                for line in r["lines"]:
                    folium.PolyLine(line, color="black", weight=5, opacity=0.85,
                                    tooltip=tip, popup=folium.Popup(info, max_width=250)).add_to(m)
                folium.Marker(
                    [r["lat"], r["lon"]],
                    popup=folium.Popup(info, max_width=250),
                    tooltip=tip,
                    icon=small_bike_icon("black")
                ).add_to(m)

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


# ═══ TAB 2: COMMUNITY ═══
with tab_community:
    st.header(t("community_header"))

    col_create, col_browse = st.columns([1, 2])

    with col_create:
        st.subheader(t("create_meetup"))
        with st.form("meetup_form"):
            title = st.text_input(t("title"), placeholder=t("title_placeholder"))
            activity = st.selectbox(t("activity"), ["Jogging", "Walking", "Cycling", "Yoga", "Workout", "Other"],
                                    format_func=opt)
            col_d, col_t = st.columns(2)
            with col_d:
                date = st.date_input(t("date"))
            with col_t:
                time = st.time_input(t("time"))
            point = st.selectbox(t("meeting_point"), AREA_NAMES)
            max_p = st.slider(t("max_participants"), 2, 50, 15)
            desc = st.text_area(t("description"))
            if st.form_submit_button(t("create_meetup_btn"), width="stretch"):
                if title:
                    st.success(t("meetup_created", title=title) + " (Demo)")
                else:
                    st.warning(t("title_missing"))

    with col_browse:
        st.subheader(t("upcoming_meetups"))

        emojis = {"Jogging": "🏃", "Walking": "🚶", "Cycling": "🚴", "Yoga": "🧘"}

        for mu in MEETUPS:
            emoji = emojis.get(mu["activity"], "📍")
            spots_left = mu["max"] - mu["joined"]
            mu_title, mu_desc = mu["title"], mu["desc"]
            if get_lang() == "de" and mu["id"] in MEETUPS_DE:
                mu_title, mu_desc = MEETUPS_DE[mu["id"]]

            st.markdown(f"""
            ### {emoji} {mu_title}
            📅 {t('date_at_time', date=mu['date'], time=mu['time'])} | 📍 {mu['point']}
            {mu_desc}
            👤 **{mu['joined']}/{mu['max']}** {t('joined_count', n=spots_left)}
            *{t('organized_by', name=mu['organizer'])}*
            """)

            if st.button(t("join_event"), key=f"join_{mu['id']}"):
                st.success(t("joined") + " (Demo)")
            st.divider()


# ═══ TAB 3: RATE & REPORT ═══
with tab_rate:
    st.header(t("rate_header"))

    rate_tab, ideas_tab = st.tabs([t("subtab_rate"), t("subtab_ideas")])

    # ─── Sub-tab: Rate & Report ───
    with rate_tab:
        col_form, col_reviews = st.columns(2)

        with col_form:
            st.subheader(t("rate_spot"))
            with st.form("rate_form"):
                spot = st.selectbox(t("select_spot"), AREA_NAMES)
                rating = st.slider(t("rating"), 1, 5, 3, format="%d ⭐")
                comment = st.text_area(t("your_experience"))

                report = st.checkbox(t("report_issue"))
                if report:
                    issue = st.selectbox(t("issue"),
                        ["Broken fountain", "No shade", "Trash", "Unsafe", "Needs seating", "Needs water"],
                        format_func=opt)

                if st.form_submit_button(t("submit"), width="stretch"):
                    st.success(t("thanks_demo"))

            st.subheader(t("suggest_improvement"))
            with st.form("suggest_form"):
                suggestion = st.selectbox(t("whats_needed"),
                    ["More trees", "Water fountain", "Cooling station", "Benches", "Better lighting",
                     "Pet water station", "Sensor box", "Mist cooling zone"], format_func=opt)
                where = st.selectbox(t("where"), AREA_NAMES, key="suggest_where")
                urgency = st.select_slider(t("urgency"), ["Nice to have", "Would help", "Needed", "Urgent"],
                                           format_func=opt)
                if st.form_submit_button(t("submit_suggestion"), width="stretch"):
                    st.success(t("recorded_demo"))

        with col_reviews:
            st.subheader(t("community_ratings"))
            for r in RATINGS:
                stars = "⭐" * int(r["rating"])
                label = t("label_great") if r["rating"] >= 4 else t("label_ok") if r["rating"] >= 3 else t("label_avoid")
                rating_comment = r["comment"]
                if get_lang() == "de":
                    rating_comment = RATING_COMMENTS_DE.get(r["spot"], rating_comment)
                st.markdown(f"**{r['spot']}** {stars} ({r['rating']}/5 · {r['reviews']} {t('reviews')})")
                st.caption(f'"{rating_comment}" {label}')
                st.divider()

            st.subheader(t("most_requested"))
            needs = ["Trees", "Fountains", "Benches", "Cooling", "Pet Water", "Sensors"]
            fig = px.bar(
                pd.DataFrame({"Need": [opt(n) for n in needs], "Votes": [45, 38, 31, 22, 18, 15]}),
                x="Votes", y="Need", orientation="h", color="Votes",
                color_continuous_scale=["#c8e6c9", "#2e7d32"],
                labels={"Need": t("need"), "Votes": t("votes")}
            )
            fig.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig, width="stretch")

    # ─── Sub-tab: Community Ideas Board ───
    with ideas_tab:
        st.subheader(t("subtab_ideas"))
        st.write(t("ideas_intro"))

        # Post your idea form
        with st.expander(t("post_idea"), expanded=False):
            with st.form("idea_form"):
                idea_title = st.text_input(t("idea_title"), placeholder=t("idea_title_placeholder"))
                idea_category = st.selectbox(t("category"),
                    ["Cooling Infrastructure", "Water & Drinking Fountains", "Sensor Network",
                     "Green Spaces", "Pet Friendly", "Accessibility", "Other"], format_func=opt)
                idea_location = st.selectbox(t("suggested_location"), AREA_NAMES, key="idea_loc")
                idea_desc = st.text_area(t("describe_idea"), placeholder=t("describe_idea_placeholder"))
                idea_image = st.file_uploader(t("upload_photo"), type=["png", "jpg", "jpeg"])
                if st.form_submit_button(t("post_idea_btn"), width="stretch"):
                    st.success(t("idea_posted"))

        st.divider()

        # ─── Existing community ideas ───

        # IDEA 1: Cooling Wall
        idea_header("🧊", t("idea1_title"), opt("Cooling Infrastructure"), "#2196f3", t("idea1_meta"),
                    "linear-gradient(135deg, #e3f2fd, #bbdefb)")
        col_img1, col_desc1 = st.columns([1, 2])
        with col_img1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0288d1, #4fc3f7); border-radius: 10px; padding: 2rem; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="font-size: 3rem;">🧱💧</div>
                <div style="font-size: 1.1rem; margin-top: 0.5rem;"><b>{t('idea1_card_title')}</b></div>
                <div style="font-size: 0.8rem; margin-top: 0.3rem;">{t('idea1_card_desc')}</div>
                <div style="font-size: 0.75rem; margin-top: 0.5rem; background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 5px;">{t('idea1_card_effect')}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc1:
            st.markdown(t("idea1_body"))
            idea_buttons(1, 47, 12)

        st.divider()

        # IDEA 2: Lamp Post Sensors
        idea_header("📡", t("idea2_title"), opt("Sensor Network"), "#ff9800", t("idea2_meta"),
                    "linear-gradient(135deg, #fff3e0, #ffe0b2)")
        col_img2, col_desc2 = st.columns([1, 2])
        with col_img2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e65100, #ff9800); border-radius: 10px; padding: 1rem; text-align: center; color: white; min-height: 200px;">
                <div style="font-size: 2rem; margin-bottom: 0.3rem;">🏮</div>
                <div style="font-size: 0.9rem; font-weight: bold;">{t('idea2_card_title')}</div>
                <div style="background: rgba(255,255,255,0.15); border-radius: 8px; padding: 0.5rem; margin: 0.5rem 0; text-align: left; font-size: 0.75rem;">
                    {t('idea2_card_list')}
                </div>
                <div style="font-size: 0.7rem; margin-top: 0.3rem; background: rgba(255,255,255,0.2); padding: 3px 6px; border-radius: 5px;">{t('idea2_card_power')}</div>
                <div style="font-size: 1.5rem; margin-top: 0.3rem;">🐦</div>
                <div style="font-size: 0.7rem;">{t('idea2_card_birdbox')}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc2:
            st.markdown(t("idea2_body"))
            idea_buttons(2, 63, 21)

        st.divider()

        # IDEA 3: Pet-Friendly Water Stations
        idea_header("🐕", t("idea3_title"), opt("Pet Friendly"), "#4caf50", t("idea3_meta"),
                    "linear-gradient(135deg, #e8f5e9, #c8e6c9)")
        col_img3, col_desc3 = st.columns([1, 2])
        with col_img3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2e7d32, #66bb6a); border-radius: 10px; padding: 1rem; text-align: center; color: white; min-height: 200px;">
                <div style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">{t('idea3_card_title')}</div>
                <div style="background: rgba(255,255,255,0.15); border-radius: 8px; padding: 0.5rem; font-size: 0.75rem; text-align: left;">
                    <div style="text-align: center; font-size: 2rem;">🚰</div>
                    {t('idea3_card_human')}<br><br>
                    ─ ─ ─ ─ ─ ─ ─ ─ ─<br><br>
                    <div style="text-align: center; font-size: 1.5rem;">🐾</div>
                    {t('idea3_card_pet')}
                </div>
                <div style="font-size: 0.7rem; margin-top: 0.3rem; background: rgba(255,255,255,0.2); padding: 3px 6px; border-radius: 5px;">{t('idea3_card_rain')}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc3:
            st.markdown(t("idea3_body"))
            idea_buttons(3, 52, 18)

        st.divider()

        # IDEA 4: Kids Tree Planting Initiative
        idea_header("🌱", t("idea4_title"), opt("Kids Initiative"), "#43a047", t("idea4_meta"),
                    "linear-gradient(135deg, #e8f5e9, #a5d6a7)")
        col_img4, col_desc4 = st.columns([1, 2])
        with col_img4:
            st.markdown(f"""
            <div style="background: #ffffff; border: 3px solid #43a047; border-radius: 10px; padding: 1rem; text-align: center; min-height: 280px;">
                <div style="font-size: 0.85rem; font-weight: bold; color: #2e7d32; margin-bottom: 0.5rem;">{t('idea4_card_title')}</div>
                <div style="background: #f1f8e9; border-radius: 8px; padding: 0.8rem; font-size: 0.8rem;">
                    <div style="color: #f57f17;">{t('idea4_card_hot')}</div>
                    <div style="font-size: 0.7rem; color: #888;">{t('idea4_card_where')}</div>
                    <div style="margin: 0.4rem 0;">
                        🏫 ── 🛣️🛣️🛣️🛣️ ── 🏠
                    </div>
                    <div style="font-size: 1rem;">{t('idea4_card_plant')}</div>
                    <div style="margin: 0.4rem 0;">
                        🏫 ── 🌱🌱🌱🌱 ── 🏠
                    </div>
                    <div style="font-size: 1rem;">{t('idea4_card_water')}</div>
                    <div style="margin: 0.4rem 0;">
                        🏫 ── 🌳🌳🌳🌳 ── 🏠
                    </div>
                    <div style="color: #2e7d32; font-weight: bold;">{t('idea4_card_cool')}</div>
                </div>
                <div style="font-size: 0.7rem; margin-top: 0.5rem; background: #e8f5e9; padding: 4px 8px; border-radius: 5px; color: #333;">
                    {t('idea4_card_rota')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc4:
            st.markdown(t("idea4_body"))
            idea_buttons(4, 203, 67)
            st.caption(t("idea4_top_comment"))

        st.divider()

        # IDEA 5: Elderly Crochet Shade Canopy
        idea_header("🧶", t("idea5_title"), opt("Community Project"), "#f9a825", t("idea5_meta"),
                    "linear-gradient(135deg, #fff8e1, #ffecb3)")
        col_img5, col_desc5 = st.columns([1, 2])
        with col_img5:
            try:
                st.image("canopy-5.jpg", width="stretch")
            except Exception:
                st.info(t("image_missing", file="canopy-5.jpg"))
            st.caption(t("idea5_caption"))
        with col_desc5:
            st.markdown(t("idea5_body"))
            idea_buttons(5, 112, 43)
            st.caption(t("idea5_top_comment"))


# ═══ TAB 4: DASHBOARD ═══
with tab_dashboard:
    st.header(t("dashboard_header"))
    st.caption(t("dashboard_caption", sensors=DATA_INFO["sensors"], points=f"{DATA_INFO['points']:,}",
                 first=DATA_INFO["first_day"], last=DATA_INFO["last_day"]))

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

    # Full ranking
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

    # Where the bikes measured
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

# ─── Footer ───
st.divider()
st.caption(t("footer"))
