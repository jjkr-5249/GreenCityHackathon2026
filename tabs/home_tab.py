"""🏠 Home tab: what EcoCity HN is for, key numbers, highlights from the data, and what each tab does.

All numbers come from the real measurements in real_data.py, so they update with the CSV files.
"""
import streamlit as st
from tabs.real_data import AREAS, DATA_INFO
from tabs.periods import short_date  # also adds the livability score columns to AREAS
from tabs.translation import t


def card(icon, title, text, background, title_color="#111"):
    """A rounded colored box with an icon (or None), a bold title and a short text."""
    icon_html = f'<div style="font-size: 1.8rem;">{icon}</div>' if icon else ""
    st.markdown(f"""
    <div style="background: {background}; padding: 1rem 1.2rem; border-radius: 12px; height: 100%; min-height: 150px;">
        {icon_html}
        <div style="font-weight: bold; font-size: 1.05rem; margin: 0.3rem 0; color: {title_color};">{title}</div>
        <div style="font-size: 0.9rem; color: #333;">{text}</div>
    </div>
    """, unsafe_allow_html=True)


# ═══ TAB: HOME ═══
def render():
    # Welcome banner with the mission
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1b5e20, #43a047 60%, #a5d6a7); color: white;
                padding: 2rem 2.2rem; border-radius: 16px; margin-bottom: 1.2rem;">
        <div style="font-size: 2rem; font-weight: bold;">{t('home_title')}</div>
        <div style="font-size: 1.1rem; margin-top: 0.6rem; max-width: 60rem;">{t('home_mission')}</div>
        <div style="font-size: 0.95rem; margin-top: 0.8rem; font-style: italic; opacity: 0.9;">{t('home_motto')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Key numbers of the data behind the app
    c1, c2, c3 = st.columns(3)
    c1.metric(t("sensor_bikes"), DATA_INFO["sensors"])
    c2.metric(t("readings"), f"{DATA_INFO['points']:,}")
    c3.metric(t("areas_ranked"), len(AREAS))
    st.caption(t("measured_by", sensors=DATA_INFO["sensors"],
                 first=short_date(DATA_INFO["first_day"], with_year=True),
                 last=short_date(DATA_INFO["last_day"], with_year=True)))

    st.divider()

    # Highlights: best areas in the measurements
    st.subheader(t("home_highlights"))
    st.caption(t("vs_city_now"))
    coolest = AREAS.loc[AREAS["temp_anom"].idxmin()]
    cleanest = AREAS.loc[AREAS["pm25_anom"].idxmin()]
    most_livable = AREAS.loc[AREAS["livability"].idxmax()]
    h1, h2, h3 = st.columns(3)
    with h1:
        card("❄️", t("home_coolest", area=coolest["label"]),
             t("temp_vs_city", v=coolest["temp_anom"]), "#e3f2fd")
    with h2:
        card("🌬️", t("home_cleanest", area=cleanest["label"]),
             t("pm_vs_city", v=cleanest["pm25_anom"]), "#e8f5e9")
    with h3:
        card("🏙️", t("home_most_livable", area=most_livable["label"]),
             f"{t('livability')}: {most_livable['livability']:.0f}/100", "#fff8e1")

    st.divider()

    # What each tab is for (the tab names already start with their icon)
    st.subheader(t("home_what_you_can_do"))
    w1, w2, w3, w4 = st.columns(4)
    with w1:
        card(None, t("tab_map"), t("home_map_text"), "#f1f8e9")
    with w2:
        card(None, t("tab_community"), t("home_community_text"), "#f3e5f5")
    with w3:
        card(None, t("tab_rate"), t("home_rate_text"), "#fff3e0")
    with w4:
        card(None, t("tab_dashboard"), t("home_dashboard_text"), "#e0f2f1")

    st.divider()

    # How the data flows back to the city
    st.subheader(t("home_how_header"))
    s1, s2, s3 = st.columns(3)
    with s1:
        card("1️⃣", t("home_step1_title"), t("home_step1_text"), "#fafafa")
    with s2:
        card("2️⃣", t("home_step2_title"), t("home_step2_text"), "#fafafa")
    with s3:
        card("3️⃣", t("home_step3_title"), t("home_step3_text"), "#fafafa")
