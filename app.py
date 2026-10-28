import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
import numpy as np
from dummy_data import SENSORS, DRINKING_WATER, COOL_SPOTS, WARM_SPOTS, SHADE_PATHS, SUNNY_PATHS, ICY_PATHS, ACCESSIBLE_PATHS, MEETUPS, RATINGS, HOURLY_TEMPS, HOURLY_PM
from real_data import AREAS, TRACKS, DATA_INFO

# ─── Page config ───
st.set_page_config(page_title="EcoCity HN", page_icon="🌿", layout="wide")

# ─── Sidebar ───
with st.sidebar:
    st.title("🌿 EcoCity HN")
    st.caption("Making Heilbronn liveable")
    st.divider()
    
    season = st.toggle("Winter Mode ❄️", value=False)
    st.divider()
    
    st.subheader("Map Layers")
    show_temp = st.checkbox("Temperature", value=True)
    show_water = st.checkbox("Drinking Water", value=True)
    # Same checkbox, different layer depending on the season
    show_spots = st.checkbox("Warm Spots" if season else "Cool Spots", value=True)
    show_paths = st.checkbox("Sunny Paths" if season else "Shaded Paths", value=True)
    show_ice = False
    if season:
        show_ice = st.checkbox("Icy Route Warnings ⚠️", value=True)
    show_access = st.checkbox("Accessible Routes ♿", value=False)
    show_air = st.checkbox("Air Quality", value=False)

    st.divider()
    st.subheader("Real Measurements")
    show_real = st.checkbox("Measured Areas 📡", value=True)
    real_by = "Temperature"
    if show_real:
        real_by = st.radio("Color areas by", ["Temperature", "Fine dust (PM2.5)"])
    show_tracks = st.checkbox("Bike Sensor Tracks", value=False)

    st.divider()
    st.caption("Green City Heilbronn Hackathon 2026")

# ─── Tabs ───
tab_map, tab_community, tab_rate, tab_dashboard = st.tabs([
    "🗺️ City Map", "👥 Community", "⭐ Rate & Report", "📊 Dashboard"
])

# ─── Session state for selected spot ───
if "selected_spot" not in st.session_state:
    st.session_state.selected_spot = None

# ═══ TAB 1: MAP ═══
with tab_map:
    st.header("☀️ Heilbronn Climate Map" if not season else "❄️ Heilbronn Climate Map")

    # Which sensor columns to use for the current season
    temp_col = "temp_winter" if season else "temperature"
    comfort_col = "comfort_winter" if season else "comfort"

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Temp", f"{SENSORS[temp_col].mean():.1f}°C")
    c2.metric("Avg Humidity", f"{SENSORS['humidity'].mean():.0f}%")
    c3.metric("Avg PM2.5", f"{SENSORS['pm25'].mean():.1f} µg/m³")
    c4.metric("Comfort", f"{SENSORS[comfort_col].mean():.0f}/100")

    # Layout: spots list on left, map on right
    col_spots, col_map = st.columns([1, 3])

    sorted_s = SENSORS.sort_values(temp_col)

    with col_spots:
        st.subheader("🔥 Warmest" if season else "🔥 Hottest")
        for _, r in sorted_s.tail(5).iloc[::-1].iterrows():
            if st.button(f"🔴 {r['name']} — {r[temp_col]}°C", key=f"hot_{r['id']}", width="stretch"):
                st.session_state.selected_spot = r['id']

        st.subheader("🥶 Coldest" if season else "❄️ Coolest")
        for _, r in sorted_s.head(5).iterrows():
            if st.button(f"🔵 {r['name']} — {r[temp_col]}°C", key=f"cool_{r['id']}", width="stretch"):
                st.session_state.selected_spot = r['id']

        if show_ice:
            st.subheader("⚠️ Icy Spots")
            for i in ICY_PATHS:
                risk = "🔴 High risk" if i["risk"] == "high" else "🟠 Medium risk"
                st.markdown(f"**{i['name']}**  \n{risk}")
                st.caption(i["reason"])

        if show_paths and season:
            st.subheader("☀️ Sunny Paths")
            for p in SUNNY_PATHS:
                st.markdown(f"**{p['name']}**  \n{p['sun']}% sun · {p['length_km']} km")
                st.caption(p["desc"])

        if show_paths and not season:
            st.subheader("🌳 Shaded Paths")
            for p in SHADE_PATHS:
                st.markdown(f"**{p['name']}**  \n{p['shade']}% shade · {p['length_km']} km")
                st.caption(p["desc"])

        if show_access:
            st.subheader("♿ Accessible Routes")
            st.caption("Smooth routes for wheelchairs and strollers")
            for a in ACCESSIBLE_PATHS:
                steps = "✅ Step-free" if a["step_free"] else "⚠️ Has obstacles"
                st.markdown(f"**{a['name']}**  \n{steps} · {a['surface']} · max {a['max_slope']}% slope · {a['length_km']} km")
                if season:
                    st.markdown("❄️ Cleared of snow first" if a["cleared"] else "❄️ Not cleared, may be icy")
                st.caption(a["desc"])

        if st.session_state.selected_spot:
            if st.button("🔄 Reset View", width="stretch"):
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

        # With real data on, zoom so all measured areas fit (outer towns included)
        if show_real and not selected:
            m.fit_bounds([[AREAS["lat"].min(), AREAS["lon"].min()],
                          [AREAS["lat"].max(), AREAS["lon"].max()]])

        # Temperature heatmap
        if show_temp:
            from folium.plugins import HeatMap
            # Scale temperatures to 0..1 (coldest..warmest) so negative winter values work too
            low, high = SENSORS[temp_col].min(), SENSORS[temp_col].max()
            heat_data = [[r["lat"], r["lon"], (r[temp_col] - low) / (high - low)] for _, r in SENSORS.iterrows()]
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
                tooltip=f"📍 Selected: {spot_row['name']}"
            ).add_to(m)
        
        # Sensor markers
        for _, r in SENSORS.iterrows():
            is_selected = (selected == r["id"])
            t = r[temp_col]
            if season:
                color = "blue" if t < 0 else "lightblue" if t < 2 else "orange"
            else:
                color = "blue" if t < 29 else "orange" if t < 33 else "red"

            popup = f"""<b>{r['name']}</b><br>
            🌡️ {t}°C<br>
            💧 {r['humidity']}%<br>
            🌬️ PM2.5: {r['pm25']} µg/m³<br>
            PM10: {r['pm10']} µg/m³<br>
            ⭐ Comfort: {r[comfort_col]}/100"""
            
            if is_selected:
                icon = folium.Icon(color="cadetblue", icon="star", prefix="fa")
            else:
                icon = folium.Icon(color=color, icon="thermometer-half", prefix="fa")
            
            folium.Marker(
                [r["lat"], r["lon"]],
                popup=popup,
                tooltip=f"{r['name']}: {t}°C",
                icon=icon
            ).add_to(m)
        
        # Water spots
        if show_water:
            for w in DRINKING_WATER:
                color = "blue" if w["status"] == "working" else "red" if w["status"] == "broken" else "gray"
                status = "✅" if w["status"] == "working" else "❌" if w["status"] == "broken" else "⚠️"
                folium.Marker(
                    [w["lat"], w["lon"]],
                    popup=f"💧 {w['name']}<br>Status: {status} {w['status']}",
                    tooltip=f"💧 {w['name']} ({status})",
                    icon=folium.Icon(color=color, icon="tint", prefix="fa")
                ).add_to(m)
        
        # Warm spots (winter)
        if show_spots and season:
            icons = {"library": "book", "shopping": "shopping-bag", "warming_room": "coffee"}
            for w in WARM_SPOTS:
                folium.Marker(
                    [w["lat"], w["lon"]],
                    popup=f"🔥 <b>{w['name']}</b><br>{w['desc']}<br>🕒 {w['hours']}",
                    tooltip=f"🔥 {w['name']}",
                    icon=folium.Icon(color="orange", icon=icons[w["type"]], prefix="fa")
                ).add_to(m)

        # Cool spots (summer)
        if show_spots and not season:
            for s in COOL_SPOTS:
                folium.Marker(
                    [s["lat"], s["lon"]],
                    popup=f"🌳 {s['name']}<br>{s['desc']}",
                    tooltip=f"🌳 {s['name']}",
                    icon=folium.Icon(color="green", icon="tree", prefix="fa")
                ).add_to(m)
        
        # Shaded paths: dark green = very shady, light green = partly shady
        if show_paths and not season:
            for p in SHADE_PATHS:
                color = "#1b5e20" if p["shade"] >= 75 else "#66bb6a"
                folium.PolyLine(
                    p["points"], color=color, weight=6, opacity=0.8,
                    tooltip=f"🌳 {p['name']} — {p['shade']}% shade, {p['length_km']} km",
                    popup=f"<b>{p['name']}</b><br>{p['desc']}"
                ).add_to(m)

        # Sunny paths (winter): dark yellow = very sunny, light yellow = partly sunny
        if show_paths and season:
            for p in SUNNY_PATHS:
                color = "#f9a825" if p["sun"] >= 75 else "#ffd54f"
                folium.PolyLine(
                    p["points"], color=color, weight=6, opacity=0.9,
                    tooltip=f"☀️ {p['name']} — {p['sun']}% sun, {p['length_km']} km",
                    popup=f"<b>{p['name']}</b><br>{p['desc']}"
                ).add_to(m)

        # Where the sensor bikes rode, as a purple heatmap
        if show_tracks:
            from folium.plugins import HeatMap
            # log scale, so busy roads don't hide the quiet ones (n goes from 1 to ~8000)
            weight = np.log1p(TRACKS["n"]) / np.log1p(TRACKS["n"].max())
            track_data = list(zip(TRACKS["lat"], TRACKS["lon"], weight))
            HeatMap(track_data, radius=6, blur=4, min_opacity=0.4,
                    gradient={0.2: "#d1c4e9", 0.6: "#7e57c2", 1.0: "#311b92"}).add_to(m)

        # Real measured areas (openSenseMap bike sensors)
        if show_real:
            for _, a in AREAS.iterrows():
                if real_by == "Temperature":
                    # blue = cooler than the rest of the city at the same hour, orange = warmer
                    color = "#1565c0" if a["temp_anom"] < -0.2 else "#64b5f6" if a["temp_anom"] < 0 else "#fb8c00"
                else:
                    # green = cleaner air, orange/red = more fine dust than the rest of the city
                    color = "#43a047" if a["pm25_anom"] < 0.1 else "#fb8c00" if a["pm25_anom"] < 0.4 else "#e53935"
                air = "🟢 Cleaner than average" if a["pm25_anom"] < 0.1 else "🟠 Slightly worse" if a["pm25_anom"] < 0.4 else "🔴 More fine dust"
                popup = f"""<b>📡 {a['area']}</b> · Rank {a['rank_overall']} of {len(AREAS)}<br><br>
                🌡️ <b>Temperature:</b> {a['temp_mean']:.1f}°C<br>
                &nbsp;&nbsp;&nbsp;&nbsp;{a['temp_anom']:+.2f}°C vs. city at the same hour<br>
                🌬️ <b>Air quality:</b> {air}<br>
                &nbsp;&nbsp;&nbsp;&nbsp;PM2.5: {a['pm25_mean']:.1f} µg/m³ ({a['pm25_anom']:+.2f} vs. city)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;PM10: {a['pm10_mean']:.1f} µg/m³<br><br>
                <small>{a['readings']} readings · {a['days']} days · {a['riders']} bikes</small>"""
                folium.Circle(
                    [a["lat"], a["lon"]], radius=450,
                    color=color, weight=2, fill=True, fill_opacity=0.35,
                    tooltip=f"📡 {a['area']} — click for values",
                    popup=folium.Popup(popup, max_width=280)
                ).add_to(m)

                # Clickable name label in the middle of the circle
                short = a["label"]
                label = f"""<div style="transform: translate(-50%, -50%); width: max-content;
                    background: white; color: #111; border: 2px solid {color}; border-radius: 10px;
                    padding: 1px 6px; font: bold 11px sans-serif; cursor: pointer;">{short}</div>"""
                folium.Marker(
                    [a["lat"], a["lon"]],
                    icon=folium.DivIcon(html=label, icon_size=(0, 0)),
                    tooltip=f"📡 {a['area']} — click for values",
                    popup=folium.Popup(popup, max_width=280)
                ).add_to(m)

        # Icy spots (winter): dotted red line plus a snowflake marker at the start
        if show_ice:
            for i in ICY_PATHS:
                color = "#c62828" if i["risk"] == "high" else "#ef6c00"
                tip = f"⚠️ {i['name']} — {i['risk']} risk: {i['reason']}"
                folium.PolyLine(i["points"], color=color, weight=7, opacity=0.9,
                                dash_array="2, 10", tooltip=tip).add_to(m)
                folium.Marker(
                    i["points"][0], tooltip=tip,
                    icon=folium.Icon(color="red" if i["risk"] == "high" else "orange",
                                     icon="snowflake", prefix="fa")
                ).add_to(m)

        # Accessible routes: dashed so they stand out from shaded paths
        # dark blue = step-free, light blue = has some obstacles
        if show_access:
            for a in ACCESSIBLE_PATHS:
                color = "#0d47a1" if a["step_free"] else "#64b5f6"
                folium.PolyLine(
                    a["points"], color=color, weight=6, opacity=0.9, dash_array="10, 8",
                    tooltip=f"♿ {a['name']} — {a['surface']}, max {a['max_slope']}% slope",
                    popup=f"<b>{a['name']}</b><br>{a['desc']}"
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
            st.info(f"📍 **{spot_row['name']}** — {spot_row[temp_col]}°C | Humidity: {spot_row['humidity']}% | PM2.5: {spot_row['pm25']} µg/m³ | Comfort: {spot_row[comfort_col]}/100")


# ═══ TAB 2: COMMUNITY ═══
with tab_community:
    st.header("👥 Community Hub")
    
    col_create, col_browse = st.columns([1, 2])
    
    with col_create:
        st.subheader("Create a Meetup")
        with st.form("meetup_form"):
            title = st.text_input("Title", placeholder="Morning Jog along Neckar")
            activity = st.selectbox("Activity", ["Jogging", "Walking", "Cycling", "Yoga", "Workout", "Other"])
            col_d, col_t = st.columns(2)
            with col_d:
                date = st.date_input("Date")
            with col_t:
                time = st.time_input("Time")
            point = st.selectbox("Meeting Point", SENSORS["name"].tolist())
            max_p = st.slider("Max Participants", 2, 50, 15)
            desc = st.text_area("Description")
            if st.form_submit_button("Create Meetup", width="stretch"):
                st.success(f"✅ '{title}' created! (Demo)")
    
    with col_browse:
        st.subheader("Upcoming Meetups")
        
        emojis = {"Jogging": "🏃", "Walking": "🚶", "Cycling": "🚴", "Yoga": "🧘"}
        
        for mu in MEETUPS:
            emoji = emojis.get(mu["activity"], "📍")
            spots_left = mu["max"] - mu["joined"]
            
            st.markdown(f"""
            ### {emoji} {mu['title']}
            📅 {mu['date']} at {mu['time']} | 📍 {mu['point']}  
            {mu['desc']}  
            👤 **{mu['joined']}/{mu['max']}** joined ({spots_left} spots left)  
            *Organized by {mu['organizer']}*
            """)
            
            if st.button(f"Join this event", key=f"join_{mu['id']}"):
                st.success("✅ Joined! (Demo)")
            st.divider()


# ═══ TAB 3: RATE & REPORT ═══
with tab_rate:
    st.header("⭐ Rate, Report & Ideas")
    
    rate_tab, ideas_tab = st.tabs(["📝 Rate & Report", "💡 Community Ideas Board"])
    
    # ─── Sub-tab: Rate & Report ───
    with rate_tab:
        col_form, col_reviews = st.columns(2)
        
        with col_form:
            st.subheader("Rate a Spot")
            with st.form("rate_form"):
                spot = st.selectbox("Select spot", SENSORS["name"].tolist())
                rating = st.slider("Rating", 1, 5, 3, format="%d ⭐")
                comment = st.text_area("Your experience")
                
                report = st.checkbox("Report an issue")
                if report:
                    issue = st.selectbox("Issue", 
                        ["Broken fountain", "No shade", "Trash", "Unsafe", "Needs seating", "Needs water"])
                
                if st.form_submit_button("Submit", width="stretch"):
                    st.success("✅ Thanks! (Demo)")
            
            st.subheader("Suggest Improvement")
            with st.form("suggest_form"):
                suggestion = st.selectbox("What's needed?",
                    ["More trees", "Water fountain", "Cooling station", "Benches", "Better lighting",
                     "Pet water station", "Sensor box", "Mist cooling zone"])
                where = st.selectbox("Where?", SENSORS["name"].tolist(), key="suggest_where")
                urgency = st.select_slider("Urgency", ["Nice to have", "Would help", "Needed", "Urgent"])
                if st.form_submit_button("Submit Suggestion", width="stretch"):
                    st.success("✅ Recorded! (Demo)")
        
        with col_reviews:
            st.subheader("Community Ratings")
            for r in RATINGS:
                stars = "⭐" * int(r["rating"])
                label = "🟢 Great" if r["rating"] >= 4 else "🟡 OK" if r["rating"] >= 3 else "🔴 Avoid"
                st.markdown(f"**{r['spot']}** {stars} ({r['rating']}/5 · {r['reviews']} reviews)")
                st.caption(f'"{r["comment"]}" {label}')
                st.divider()
            
            st.subheader("Most Requested")
            fig = px.bar(
                pd.DataFrame({"Need": ["Trees", "Fountains", "Benches", "Cooling", "Pet Water", "Sensors"], 
                              "Votes": [45, 38, 31, 22, 18, 15]}),
                x="Votes", y="Need", orientation="h", color="Votes",
                color_continuous_scale=["#c8e6c9", "#2e7d32"]
            )
            fig.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig, width="stretch")
    
    # ─── Sub-tab: Community Ideas Board ───
    with ideas_tab:
        st.subheader("💡 Community Ideas Board")
        st.write("Citizens share ideas to make Heilbronn more liveable. Vote on ideas you support!")
        
        # Post your idea form
        with st.expander("📮 Post Your Idea", expanded=False):
            with st.form("idea_form"):
                idea_title = st.text_input("Idea Title", placeholder="e.g. Install mist cooling walls at Marktplatz")
                idea_category = st.selectbox("Category", 
                    ["Cooling Infrastructure", "Water & Drinking Fountains", "Sensor Network",
                     "Green Spaces", "Pet Friendly", "Accessibility", "Other"])
                idea_location = st.selectbox("Suggested Location", SENSORS["name"].tolist(), key="idea_loc")
                idea_desc = st.text_area("Describe your idea", placeholder="Explain what you'd like to see and why it would help...")
                idea_image = st.file_uploader("Upload a photo or sketch (optional)", type=["png", "jpg", "jpeg"])
                if st.form_submit_button("Post Idea", width="stretch"):
                    st.success("✅ Idea posted! (Demo)")
        
        st.divider()
        
        # ─── Existing community ideas ───
        
        # IDEA 1: Cooling Wall
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🧊</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">Cooling Water Walls at Hot Spots</span>
                <span style="background: #2196f3; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">Cooling Infrastructure</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">Posted by <b>Maria S.</b> · 📍 Marktplatz · 3 days ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_img1, col_desc1 = st.columns([1, 2])
        with col_img1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #0288d1, #4fc3f7); border-radius: 10px; padding: 2rem; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="font-size: 3rem;">🧱💧</div>
                <div style="font-size: 1.1rem; margin-top: 0.5rem;"><b>Cooling Water Wall</b></div>
                <div style="font-size: 0.8rem; margin-top: 0.3rem;">Vertical water features with<br>wooden frame & green facade</div>
                <div style="font-size: 0.75rem; margin-top: 0.5rem; background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 5px;">Cools surrounding area by 3-5°C</div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc1:
            st.markdown("""
            **Install water cooling walls** at Heilbronn's hottest spots like Marktplatz and Kaiserstrasse. 
            These vertical water features with wooden frames and green facades can cool the surrounding 
            area by 3-5°C through evaporative cooling. They also add greenery and improve air quality.
            
            **Why it works:** Water evaporation absorbs heat from the air. Combined with plants on the 
            facade, it creates a natural micro-climate cooling effect. Benches nearby let people sit 
            and enjoy the cooler zone.
            
            **Suggested locations:** Marktplatz (35.2°C avg), Hauptbahnhof (34.0°C avg)
            """)
            c1, c2, c3 = st.columns(3)
            c1.button("👍 47 Votes", key="vote_1", width="stretch")
            c2.button("💬 12 Comments", key="comment_1", width="stretch")
            c3.button("📍 Show on Map", key="map_1", width="stretch")
        
        st.divider()
        
        # IDEA 2: Lamp Post Sensors
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">📡</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">Smart Lamp Post Sensor Network</span>
                <span style="background: #ff9800; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">Sensor Network</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">Posted by <b>Jonas K.</b> · 📍 City-wide · 5 days ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_img2, col_desc2 = st.columns([1, 2])
        with col_img2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e65100, #ff9800); border-radius: 10px; padding: 1rem; text-align: center; color: white; min-height: 200px;">
                <div style="font-size: 2rem; margin-bottom: 0.3rem;">🏮</div>
                <div style="font-size: 0.9rem; font-weight: bold;">Smart Lamp Post</div>
                <div style="background: rgba(255,255,255,0.15); border-radius: 8px; padding: 0.5rem; margin: 0.5rem 0; text-align: left; font-size: 0.75rem;">
                    📡 senseBox mounted at top<br>
                    🌡️ Temperature + Humidity<br>
                    🌬️ PM1, PM2.5, PM4, PM10<br>
                    ⚗️ <b>NO₂ + O₃ gas sensors</b><br>
                    📍 GPS location built-in
                </div>
                <div style="font-size: 0.7rem; margin-top: 0.3rem; background: rgba(255,255,255,0.2); padding: 3px 6px; border-radius: 5px;">Powered by lamp post electricity</div>
                <div style="font-size: 1.5rem; margin-top: 0.3rem;">🐦</div>
                <div style="font-size: 0.7rem;">Bird box housing option<br>blends with environment</div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc2:
            st.markdown("""
            **Mount sensor boxes on existing lamp posts** across Heilbronn to dramatically expand our 
            environmental monitoring coverage — no new infrastructure needed!
            
            **The setup:**
            - senseBox sensor unit attached to the lamp post, powered by the existing electricity
            - Measures temperature, humidity, PM1/PM2.5/PM4/PM10 particulate matter
            - **NEW: NO₂ and O₃ gas sensors** to track traffic pollution and summer ozone
            - Bird box-style housing that blends naturally into the streetscape
            
            **Why NO₂ and O₃ matter:** NO₂ comes directly from vehicle exhaust. Ground-level ozone (O₃) 
            forms when sunlight cooks traffic fumes — it gets **worst on the hottest days**, exactly when 
            EcoCity users need the cleanest routes.
            
            **Coverage goal:** Every 200m along main roads = complete city monitoring
            """)
            c1, c2, c3 = st.columns(3)
            c1.button("👍 63 Votes", key="vote_2", width="stretch")
            c2.button("💬 21 Comments", key="comment_2", width="stretch")
            c3.button("📍 Show on Map", key="map_2", width="stretch")
        
        st.divider()
        
        # IDEA 3: Pet-Friendly Water Stations
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🐕</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">Pet-Friendly Drinking Water Stations</span>
                <span style="background: #4caf50; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">Pet Friendly</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">Posted by <b>Sophie L.</b> · 📍 Wertwiesenpark, Neckarufer · 1 week ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_img3, col_desc3 = st.columns([1, 2])
        with col_img3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #2e7d32, #66bb6a); border-radius: 10px; padding: 1rem; text-align: center; color: white; min-height: 200px;">
                <div style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">Pet-Friendly Fountain</div>
                <div style="background: rgba(255,255,255,0.15); border-radius: 8px; padding: 0.5rem; font-size: 0.75rem; text-align: left;">
                    <div style="text-align: center; font-size: 2rem;">🚰</div>
                    <b>Human level:</b><br>
                    Standard drinking fountain<br>
                    with bottle refill tap<br><br>
                    ─ ─ ─ ─ ─ ─ ─ ─ ─<br><br>
                    <div style="text-align: center; font-size: 1.5rem;">🐾</div>
                    <b>Ground level:</b><br>
                    Sliding panel opens to<br>
                    reveal water bowl for pets<br>
                    Auto-drain & self-cleaning
                </div>
                <div style="font-size: 0.7rem; margin-top: 0.3rem; background: rgba(255,255,255,0.2); padding: 3px 6px; border-radius: 5px;">♻️ Rainwater collection option</div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc3:
            st.markdown("""
            **Dual-level drinking fountains** that serve both people and their pets! Perfect for 
            Heilbronn's parks and walking paths along the Neckar.
            
            **Design features:**
            - **Upper level:** Standard drinking fountain + bottle refill spout for humans
            - **Lower level:** Sliding panel at the base that opens to reveal a stainless steel water bowl for dogs and cats
            - **Hygienic:** Auto-drain after each use, self-cleaning cycle, fresh water each time
            - **Sustainable:** Optional rainwater collection system for the pet bowl
            
            **Why this matters:** On hot summer days, dogs suffer from heat too. Dog owners currently 
            carry extra water or look for puddles. These stations make walks safer for pets and encourage 
            people to walk longer cool routes instead of cutting through hot zones.
            
            **Suggested locations:** Wertwiesenpark (popular dog walking), Neckarufer paths, Pfuehlpark
            """)
            c1, c2, c3 = st.columns(3)
            c1.button("👍 52 Votes", key="vote_3", width="stretch")
            c2.button("💬 18 Comments", key="comment_3", width="stretch")
            c3.button("📍 Show on Map", key="map_3", width="stretch")
        
        st.divider()
        
        # IDEA 4: Kids Tree Planting Initiative
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e9, #a5d6a7); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🌱</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">Cool Our School Road! — Sapling Squad 🌳</span>
                <span style="background: #43a047; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">Kids Initiative</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">Posted by <b>Class 4a, Grundschule Dammstrasse</b> 👧👦 · Ages 9-10 · 📍 Kaiserstrasse & Dammstrasse · 5 days ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_img4, col_desc4 = st.columns([1, 2])
        with col_img4:
            st.markdown("""
            <div style="background: #ffffff; border: 3px solid #43a047; border-radius: 10px; padding: 1rem; text-align: center; min-height: 280px;">
                <div style="font-size: 0.85rem; font-weight: bold; color: #2e7d32; margin-bottom: 0.5rem;">🌱 The Sapling Squad Plan 🌱</div>
                <div style="background: #f1f8e9; border-radius: 8px; padding: 0.8rem; font-size: 0.8rem;">
                    <div style="color: #f57f17;">☀️ HOT ROAD (34°C) ☀️</div>
                    <div style="font-size: 0.7rem; color: #888;">Kaiserstrasse near school</div>
                    <div style="margin: 0.4rem 0;">
                        🏫 ── 🛣️🛣️🛣️🛣️ ── 🏠
                    </div>
                    <div style="font-size: 1rem;">⬇️ We plant! ⬇️</div>
                    <div style="margin: 0.4rem 0;">
                        🏫 ── 🌱🌱🌱🌱 ── 🏠
                    </div>
                    <div style="font-size: 1rem;">⬇️ We water daily! ⬇️</div>
                    <div style="margin: 0.4rem 0;">
                        🏫 ── 🌳🌳🌳🌳 ── 🏠
                    </div>
                    <div style="color: #2e7d32; font-weight: bold;">🌡️ COOL ROAD! 🌡️</div>
                </div>
                <div style="font-size: 0.7rem; margin-top: 0.5rem; background: #e8f5e9; padding: 4px 8px; border-radius: 5px; color: #333;">
                    📅 Mon: Team A 💧 Tue: Team B 💧<br>
                    📅 Wed: Team C 💧 Thu: Team D 💧<br>
                    📅 Fri: Team E 💧<br>
                    📅 Sat: Neighborhood kids 🏡💧<br>
                    📅 Sun: Neighborhood kids 🏡💧<br>
                    ✅ Every day covered!
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_desc4:
            st.markdown("""
            *"Hello! We are Class 4a and on Environment Day our teacher showed us the EcoCity app. 
            We checked — the road from our school to the bus stop is 34°C in summer! There are 
            NO trees at all. So we have a plan!"* 🌱
            
            **Our "Sapling Squad" Plan:**
            - **Plant tree saplings** along Kaiserstrasse and Dammstrasse near our school
            - **We take care of them!** Every class gets a watering schedule — Team A on Monday, 
              Team B on Tuesday, Team C on Wednesday... every day is covered
            - Each student "adopts" a sapling and gives it a name 
            - We measure the temperature next to our trees every week using a thermometer 
              and track it on the EcoCity app
            - **Next year's Class 4 takes over** — so the trees always have caretakers!
            
            **What we need from the city:**
            - Saplings (we researched: linden trees and maples grow well in Heilbronn!)
            - Permission to plant along the school road
            - A few watering cans for the school 
            
            *"Our teacher Herr Weber says if each class plants 10 trees, in 5 years the 
            whole road will be shaded. We did the math — that's 50 trees from just our 
            school! And if other schools join..."* 🌳🌳🌳
            
            **Herr Weber's note:** *"This project teaches the children responsibility, teamwork, 
            and climate science. They've already used EcoCity data to identify the hottest 
            streets near school. The daily watering rota is their own idea — I'm very proud."*
            """)
            c1, c2, c3 = st.columns(3)
            c1.button("👍 203 Votes", key="vote_4", width="stretch")
            c2.button("💬 67 Comments", key="comment_4", width="stretch")
            c3.button("📍 Show on Map", key="map_4", width="stretch")
            st.caption('💬 Top comment: *"This is what education should look like. Our school wants to join — can we make this city-wide?"* — Frau Müller, Elly-Heuss-Knapp Gymnasium')
        
        st.divider()
        
        # IDEA 5: Elderly Crochet Shade Canopy
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff8e1, #ffecb3); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🧶</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">Crochet Shade Canopy — Let Us Knit Heilbronn Cool!</span>
                <span style="background: #f9a825; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">Community Project</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">Posted by <b>Ingrid H., 67</b> 👵 · Heilbronn Strickgruppe "Goldene Nadeln" · 📍 Marktplatz, Kaiserstrasse · 2 days ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_img5, col_desc5 = st.columns([1, 2])
        with col_img5:
            try:
                st.image("canopy-5.jpg", width="stretch")
            except:
                st.info("📷 Image: canopy-5.jpg not found — place it in the ecocity-hn folder")
            st.caption("📸 Reference: Tejiendo la Calle, Valverde de la Vera & Alhaurín de la Torre, Spain")
        with col_desc5:
            st.markdown("""
            *"Liebe Heilbronner! Our knitting circle has 25 members, ages 58 to 82. We've been meeting 
            every Wednesday for years. When we saw what the women in Spain did — crocheting beautiful 
            shade canopies over their streets — we said: WE CAN DO THIS TOO!"* 👵🧶
            
            **Our proposal:**
            - Our group "Goldene Nadeln" will crochet colorful shade panels from recycled yarn
            - We string them between buildings over Kaiserstrasse and Marktplatz in summer
            - Each panel is a unique artwork — we'll weave in Heilbronn landmarks and patterns
            - **We just need the city to provide yarn and the hanging infrastructure!**
            
            **Why it works — proven in Spain:**
            In Valverde de la Vera, elderly women created "Tejiendo la Calle" (Knitting the Street) — 
            XXL crochet sunshades that cool streets by up to 5°C. In Alhaurín de la Torre near Malaga, 
            40 women crocheted a 13,000 sq ft canopy over the shopping street. Both projects won 
            European awards.
            
            **What we bring:** Community spirit, skilled hands, and time. What we need: yarn, 
            metal cables between buildings, and the city's blessing. 
            
            **If this project gets accepted, we'll need more hands!** We will post a meetup in the 
            Community Hub to recruit new members — all ages welcome, beginners too. We'll teach you! 🧶
            
            Let's knit Heilbronn cool! 🧶❤️
            """)
            c1, c2, c3 = st.columns(3)
            c1.button("👍 112 Votes", key="vote_5", width="stretch")
            c2.button("💬 43 Comments", key="comment_5", width="stretch")
            c3.button("📍 Show on Map", key="map_5", width="stretch")
            st.caption("💬 Top comment: *\"This is the most beautiful idea! My Oma wants to join!\"* — Lena, 29")
        


# ═══ TAB 4: DASHBOARD ═══
with tab_dashboard:
    st.header("📊 July 2026 Analysis")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sensors", "15")
    c2.metric("Hot Days (>35°C)", "12")
    c3.metric("Coolest Spot", "Waldgebiet (26.2°C)")
    c4.metric("Worst Air", "Industrie (28.4 µg/m³)")
    
    st.divider()
    
    # Temperature chart
    fig1 = px.line(HOURLY_TEMPS, x="hour", y="temperature", color="type",
                   title="Typical Daily Temperature by Area Type",
                   labels={"temperature": "°C", "hour": "Hour"})
    fig1.update_layout(height=350)
    st.plotly_chart(fig1, width="stretch")
    
    # PM chart
    col_pm, col_bar = st.columns(2)
    
    with col_pm:
        fig2 = px.line(HOURLY_PM, x="hour", y="pm25", color="type",
                       title="PM2.5 Throughout the Day",
                       labels={"pm25": "µg/m³", "hour": "Hour"})
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, width="stretch")
    
    with col_bar:
        fig3 = px.bar(SENSORS.sort_values("temperature"), x="name", y="temperature",
                      color="temperature", color_continuous_scale=["#2196f3", "#ff9800", "#f44336"],
                      title="Temperature by Location")
        fig3.update_layout(height=300, xaxis_tickangle=-45)
        st.plotly_chart(fig3, width="stretch")
    
    st.divider()
    
    # Gap analysis
    st.subheader("🎯 Where Heilbronn Needs Help")
    
    col_gaps, col_recs = st.columns(2)
    
    with col_gaps:
        st.markdown("**Hottest areas with least infrastructure:**")
        hot = SENSORS[SENSORS["temperature"] > 33].sort_values("temperature", ascending=False)
        for _, r in hot.iterrows():
            st.write(f"🔴 **{r['name']}** — {r['temperature']}°C, comfort {r['comfort']}/100")
    
    with col_recs:
        st.markdown("**Recommendations:**")
        recs = [
            "🌳 Plant trees at **Neckargartach Industrie** — hottest, worst air",
            "💧 Add fountain at **Kaiserstrasse** — high foot traffic, no water",
            "🏗️ Shade structure at **Hauptbahnhof** — transit hub, people wait in heat",
            "🔧 Fix fountain at **Pfuehlpark** — reported broken",
            "🌳 Expand canopy at **Marktplatz** — tourist area, consistently hot",
        ]
        for r in recs:
            st.write(r)
    
    st.divider()
    
    # Real measurements: area ranking
    st.subheader("📡 Real Measurements: Area Ranking")
    st.caption(
        f"openSenseMap bike sensors · {DATA_INFO['sensors']} bikes · "
        f"{DATA_INFO['points']:,} readings · {DATA_INFO['first_day']} to {DATA_INFO['last_day']}. "
        "Rank 1 = coolest and cleanest. Differences are compared with all sensors at the same hour."
    )
    st.dataframe(
        AREAS[["rank_overall", "area", "temp_anom", "temp_mean", "pm25_anom", "pm25_mean", "readings", "days"]],
        column_config={
            "rank_overall": "Rank",
            "area": "Area",
            "temp_anom": st.column_config.NumberColumn("Temp diff (°C)", format="%+.2f"),
            "temp_mean": st.column_config.NumberColumn("Avg temp (°C)", format="%.1f"),
            "pm25_anom": st.column_config.NumberColumn("PM2.5 diff (µg/m³)", format="%+.2f"),
            "pm25_mean": st.column_config.NumberColumn("Avg PM2.5 (µg/m³)", format="%.1f"),
            "readings": "Readings",
            "days": "Days",
        },
        hide_index=True, width="stretch",
    )
    st.caption("The gaps between areas are small (a few tenths of a degree), so read the ranking as a tendency.")

    st.divider()

    # Sensor coverage map
    st.subheader("📡 Sensor Coverage & Green Zone Gaps")
    st.write("Green circles show sensor coverage (~300m). Gaps indicate areas needing additional sensors or green infrastructure.")
    
    cov_map = folium.Map(location=[49.1427, 9.2109], zoom_start=14, tiles="OpenStreetMap")
    
    for _, loc in SENSORS.iterrows():
        # Coverage circle
        folium.Circle(
            [loc["lat"], loc["lon"]],
            radius=300,
            color="#4caf50",
            fill=True,
            fill_opacity=0.15,
            tooltip=f"{loc['name']} — {loc['type']}"
        ).add_to(cov_map)
        
        # Sensor marker
        folium.Marker(
            [loc["lat"], loc["lon"]],
            tooltip=f"📡 {loc['name']}",
            icon=folium.Icon(color="green", icon="signal", prefix="fa")
        ).add_to(cov_map)
    
    # Mark areas with NO coverage as red zones
    gap_zones = [
        {"name": "Horkheim", "lat": 49.1250, "lon": 9.2000, "reason": "No sensors, residential area"},
        {"name": "Frankenbach", "lat": 49.1650, "lon": 9.2100, "reason": "No sensors, growing suburb"},
        {"name": "Klingenberg", "lat": 49.1550, "lon": 9.2350, "reason": "No sensors, near highway"},
        {"name": "Südstadt", "lat": 49.1330, "lon": 9.2150, "reason": "No sensors, dense housing"},
    ]
    
    for gap in gap_zones:
        folium.Circle(
            [gap["lat"], gap["lon"]],
            radius=400,
            color="#f44336",
            fill=True,
            fill_opacity=0.2,
            tooltip=f"⚠️ GAP: {gap['name']} — {gap['reason']}"
        ).add_to(cov_map)
        
        folium.Marker(
            [gap["lat"], gap["lon"]],
            tooltip=f"⚠️ {gap['name']}: {gap['reason']}",
            icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
        ).add_to(cov_map)
    
    st_folium(cov_map, height=450, use_container_width=True)
    
    st.markdown("""
    **Legend:**  
    🟢 Green circles = current sensor coverage (~300m radius)  
    🔴 Red zones = coverage gaps — priority areas for new sensors or green infrastructure
    """)

# ─── Footer ───
st.divider()
st.caption("🌿 EcoCity HN — Green City Heilbronn Hackathon | Data: openSenseMap · Sensor.Community · Open-Meteo")