"""EcoCity HN: the main page. Run with `make run` (or `streamlit run app.py`) from the project root.

This file only builds the frame of the website: page setup, the ENG / DE switch,
the sidebar (on the right) and the tabs. Each tab's content is in its own file in tabs/.
"""
import streamlit as st
from tabs.real_data import BUMPY_ROADS, BUMPY_ON_MAP, DATA_INFO
from tabs.periods import PERIODS, period_label, short_date
from tabs.translation import t
from tabs import home_tab, map_tab, community_tab, rate_report_tab, dashboard_tab

# ─── Page config ───
st.set_page_config(page_title="EcoCity HN", page_icon="🌿", layout="wide")

# ─── Page layout CSS ───
st.markdown("""
<style>
/* Language switch: in the top bar, just left of Deploy (room left for "Running… Stop").
   "absolute" places it in the main area, so it follows the top bar when the sidebar opens or closes. */
.st-key-lang_switch {
    position: absolute;
    top: 1.1rem;
    right: 16rem;
    width: auto !important;
    z-index: 999991;
}

/* Sidebar on the right instead of the left */
[data-testid="stAppViewContainer"] { flex-direction: row-reverse; }
/* closed sidebar slides out to the right (Streamlit slides it to the left) */
[data-testid="stSidebar"][data-collapsed="true"] { transform: translateX(100vw) !important; }
/* close button on the inner (left) side of the sidebar, arrows pointing the other way */
[data-testid="stSidebarHeader"] { flex-direction: row-reverse; }
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] { display: inline-block; transform: scaleX(-1); }
/* open button in the top right corner; Deploy and the menu move left to make room */
[data-testid="stExpandSidebarButton"] { position: absolute; top: 1rem; right: 0.75rem; }
[data-testid="stToolbar"] { padding-right: 2.75rem; }

/* Autumn background: cream at the top fading into soft apricot (base colors are in .streamlit/config.toml) */
[data-testid="stApp"], [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"] {
    background: linear-gradient(180deg, #FFF4E6 0%, #FCE3C4 55%, #F8CFA0 100%);
}
[data-testid="stMainBlockContainer"] > div { background: transparent; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #F5D9B8 0%, #EDB98A 100%); }
[data-baseweb="tab-list"], [data-baseweb="tab-panel"] { background: transparent; }
</style>
""", unsafe_allow_html=True)
# ENG / DE switch, placed by the .st-key-lang_switch CSS above; t() reads its value (key "lang_de")
with st.container(key="lang_switch"):
    st.toggle("ENG / DE", key="lang_de", help="English ⇄ Deutsch")

# ─── Sidebar: map layers for the City Map tab ───
with st.sidebar:
    st.title("🌿 EcoCity HN")
    st.caption(t("tagline"))
    st.divider()

    st.subheader(t("time_period"))
    # the key keeps the chosen period when the label changes language
    period = st.selectbox(t("show_data_from"), PERIODS, format_func=period_label, key="period")
    st.caption(t("all_data", first=short_date(DATA_INFO["first_day"], with_year=True),
                 last=short_date(DATA_INFO["last_day"], with_year=True)))
    st.divider()

    st.subheader(t("map_layers"))
    show_real = st.checkbox(t("layer_real"), value=True)
    real_by = "livability"  # default when the real-data layer is off
    if show_real:
        real_by = st.radio(t("color_by"), ["livability", "temperature", "pm25"],
                           format_func=lambda key: t(f"color_{key}"))
        if real_by == "livability":
            st.caption(t("livability_legend"))
    show_tracks = st.checkbox(t("layer_tracks"), value=False)
    show_bike_streets = st.checkbox(t("layer_bike_streets"), value=True)
    show_access = st.checkbox(t("layer_access"), value=False)
    show_bumpy = st.checkbox(t("layer_bumpy"), value=True)
    # bumpy roads whose name is not in the road network can't be drawn
    missing = len(BUMPY_ROADS) - len(BUMPY_ON_MAP)
    if show_bumpy and missing:
        st.caption(t("bumpy_missing", missing=missing, total=len(BUMPY_ROADS)))

    st.divider()
    st.caption("Green City Heilbronn Hackathon 2026")

# ─── Tabs (each tab lives in its own file in tabs/) ───
# Only the open tab is drawn (tab.open). A map drawn in a hidden tab can't measure its size
# and zooms out to the whole world, so this keeps the maps correct and the page faster.
tab_labels = [t("tab_home"), t("tab_map"), t("tab_community"), t("tab_rate"), t("tab_dashboard")]
# The tabs are told which one to open by its label, and the labels change with the language:
# remember the open tab by its position, so an ENG / DE switch reopens the same tab
open_tab = st.session_state.get("open_tab", 0)
tab_home, tab_map, tab_community, tab_rate, tab_dashboard = st.tabs(
    tab_labels, default=tab_labels[open_tab], key=f"main_tabs_{st.session_state.get('lang_de', False)}",
    on_change="rerun")
st.session_state.open_tab = next(i for i, tab in enumerate(
    [tab_home, tab_map, tab_community, tab_rate, tab_dashboard]) if tab.open)

# Draw only the open tab (see above)
if tab_home.open:
    with tab_home:
        home_tab.render()

if tab_map.open:
    with tab_map:
        map_tab.render(period, show_real, real_by, show_tracks, show_bike_streets, show_access, show_bumpy)

if tab_community.open:
    with tab_community:
        community_tab.render()

if tab_rate.open:
    with tab_rate:
        rate_report_tab.render()

if tab_dashboard.open:
    with tab_dashboard:
        dashboard_tab.render()

# ─── Footer ───
st.divider()
st.caption(t("footer"))
