"""👥 Community tab: create a meetup and browse upcoming meetups (demo, nothing is saved yet)."""
import streamlit as st
from tabs.community_examples import MEETUPS
from tabs.real_data import AREA_NAMES
from tabs.translation import t, opt, get_lang, MEETUPS_DE

ACTIVITY_EMOJIS = {"Jogging": "🏃", "Walking": "🚶", "Cycling": "🚴", "Yoga": "🧘"}  # anything else gets 📍


# ═══ TAB: COMMUNITY ═══
def render():
    st.header(t("community_header"))

    col_create, col_browse = st.columns([1, 2])

    # Left: form to create a meetup
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

    # Right: list of example meetups (German text from MEETUPS_DE when DE is on)
    with col_browse:
        st.subheader(t("upcoming_meetups"))

        for mu in MEETUPS:
            emoji = ACTIVITY_EMOJIS.get(mu["activity"], "📍")
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
