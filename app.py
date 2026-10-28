import streamlit as st
from translation import t
from tabs import map_tab, community_tab, rate_report_tab, dashboard_tab

# ─── Page config ───
st.set_page_config(page_title="EcoCity HN", page_icon="🌿", layout="wide")

# ─── Language switch (pinned in the top bar next to Deploy; off = English, on = German) ───
st.markdown("""
<style>
.st-key-lang_switch {
    position: fixed;
    top: 1.1rem;
    right: 13.5rem;  /* leaves room for Streamlit's "Running… Stop" indicator */
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

    season = st.toggle(t("winter_mode"), value=False, key="winter_mode")
    st.divider()

    st.subheader(t("map_layers"))
    show_temp = st.checkbox(t("layer_temp"), value=True, key="show_temp")
    show_water = st.checkbox(t("layer_water"), value=True, key="show_water")
    show_cool = st.checkbox(t("layer_cool"), value=True, key="show_cool")
    show_air = st.checkbox(t("layer_air"), value=False, key="show_air")

    st.divider()
    st.caption("Green City Heilbronn Hackathon 2026")

# ─── Tabs (each tab lives in its own file in tabs/) ───
tab_map, tab_community, tab_rate, tab_dashboard = st.tabs([
    t("tab_map"), t("tab_community"), t("tab_rate"), t("tab_dashboard")
])

with tab_map:
    map_tab.render(season, show_temp, show_water, show_cool, show_air)

with tab_community:
    community_tab.render()

with tab_rate:
    rate_report_tab.render()

with tab_dashboard:
    dashboard_tab.render()

# ─── Footer ───
st.divider()
st.caption(t("footer"))
