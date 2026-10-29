"""⭐ Rate & Report tab: rate a spot, suggest an improvement, and the Community Ideas Board.

The forms are a demo (nothing is saved yet). The ideas board shows five example ideas;
their texts are in translation.py (keys idea1_... to idea5_...).
"""
from pathlib import Path

import streamlit as st
import plotly.express as px
import pandas as pd
from tabs.community_examples import RATINGS
from tabs.real_data import AREA_NAMES
from tabs.translation import t, opt, get_lang, RATING_COMMENTS_DE

# tabs/rate_report_tab.py -> project root -> images/
IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"


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


# ═══ TAB: RATE & REPORT ═══
def render():
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

                # always shown: inside a form, a checkbox can't show or hide other fields before submit
                issue = st.selectbox(t("report_issue"),
                    ["No issue", "Broken fountain", "No shade", "Trash", "Unsafe", "Needs seating", "Needs water"],
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
                st.image(str(IMAGES_DIR / "canopy-5.jpg"), width="stretch")
            except Exception:
                st.info(t("image_missing", file="canopy-5.jpg"))
            st.caption(t("idea5_caption"))
        with col_desc5:
            st.markdown(t("idea5_body"))
            idea_buttons(5, 112, 43)
            st.caption(t("idea5_top_comment"))
