import streamlit as st
from dummy_data import SENSORS, MEETUPS
from translation import t, opt, get_lang, MEETUPS_DE


# ═══ TAB 2: COMMUNITY ═══
def render():
    lang = get_lang()
    if "meetups" not in st.session_state:
        st.session_state.meetups = [dict(mu) for mu in MEETUPS]
    if "joined_ids" not in st.session_state:
        st.session_state.joined_ids = set()

    st.header(t("community_header"))

    col_create, col_browse = st.columns([1, 2])

    with col_create:
        st.subheader(t("create_meetup"))
        with st.form("meetup_form"):
            title = st.text_input(t("title"), placeholder=t("title_placeholder"), key="meetup_title")
            activity = st.selectbox(t("activity"), ["Jogging", "Walking", "Cycling", "Yoga", "Workout", "Other"],
                                    format_func=opt, key="meetup_activity")
            col_d, col_t = st.columns(2)
            with col_d:
                date = st.date_input(t("date"), key="meetup_date")
            with col_t:
                time = st.time_input(t("time"), key="meetup_time")
            point = st.selectbox(t("meeting_point"), SENSORS["name"].tolist(), key="meetup_point")
            max_p = st.slider(t("max_participants"), 2, 50, 15, key="meetup_max")
            desc = st.text_area(t("description"), key="meetup_desc")
            if st.form_submit_button(t("create_meetup_btn"), use_container_width=True):
                if not title.strip():
                    st.error(t("title_missing"))
                else:
                    new_id = max((m["id"] for m in st.session_state.meetups), default=0) + 1
                    st.session_state.meetups.insert(0, {
                        "id": new_id,
                        "title": title.strip(),
                        "activity": activity,
                        "organizer": "You",
                        "date": date.strftime("%Y-%m-%d"),
                        "time": time.strftime("%H:%M"),
                        "point": point,
                        "joined": 1,
                        "max": max_p,
                        "desc": desc.strip(),
                    })
                    st.session_state.joined_ids.add(new_id)
                    st.success(t("meetup_created", title=title))

    with col_browse:
        st.subheader(t("upcoming_meetups"))

        emojis = {"Jogging": "🏃", "Walking": "🚶", "Cycling": "🚴", "Yoga": "🧘"}

        for mu in st.session_state.meetups:
            emoji = emojis.get(mu["activity"], "📍")
            spots_left = mu["max"] - mu["joined"]
            is_demo = mu["organizer"] != "You"
            mu_title, mu_desc = mu["title"], mu["desc"]
            if lang == "de" and is_demo and mu["id"] in MEETUPS_DE:
                mu_title, mu_desc = MEETUPS_DE[mu["id"]]
            organizer = mu["organizer"] if is_demo else t("you")

            st.markdown(f"""
            ### {emoji} {mu_title}
            📅 {t('date_at_time', date=mu['date'], time=mu['time'])} | 📍 {mu['point']}
            {mu_desc}
            👤 **{mu['joined']}/{mu['max']}** {t('joined_count', n=spots_left)}
            *{t('organized_by', name=organizer)}*
            """)

            if mu["id"] in st.session_state.joined_ids:
                st.button(t("joined"), key=f"join_{mu['id']}", disabled=True)
            elif spots_left <= 0:
                st.button(t("full"), key=f"join_{mu['id']}", disabled=True)
            elif st.button(t("join_event"), key=f"join_{mu['id']}"):
                mu["joined"] += 1
                st.session_state.joined_ids.add(mu["id"])
                st.rerun()
            st.divider()
