from pathlib import Path

import streamlit as st
import plotly.express as px
import pandas as pd
from dummy_data import SENSORS, RATINGS
from translation import t, opt, get_lang, RATING_COMMENTS_DE

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"


# ═══ TAB 3: RATE & REPORT ═══
def render():
    lang = get_lang()

    st.header(t("rate_header"))

    rate_tab, ideas_tab = st.tabs([t("subtab_rate"), t("subtab_ideas")])

    # ─── Sub-tab: Rate & Report ───
    with rate_tab:
        col_form, col_reviews = st.columns(2)

        with col_form:
            st.subheader(t("rate_spot"))
            with st.form("rate_form"):
                spot = st.selectbox(t("select_spot"), SENSORS["name"].tolist(), key="rate_spot")
                rating = st.slider(t("rating"), 1, 5, 3, format="%d ⭐", key="rate_rating")
                comment = st.text_area(t("your_experience"), key="rate_comment")

                report = st.checkbox(t("report_issue"), key="rate_report")
                if report:
                    issue = st.selectbox(t("issue"),
                        ["Broken fountain", "No shade", "Trash", "Unsafe", "Needs seating", "Needs water"],
                        format_func=opt, key="rate_issue")

                if st.form_submit_button(t("submit"), use_container_width=True):
                    st.success(t("thanks_demo"))

            st.subheader(t("suggest_improvement"))
            with st.form("suggest_form"):
                suggestion = st.selectbox(t("whats_needed"),
                    ["More trees", "Water fountain", "Cooling station", "Benches", "Better lighting",
                     "Pet water station", "Sensor box", "Mist cooling zone"],
                    format_func=opt, key="suggest_what")
                where = st.selectbox(t("where"), SENSORS["name"].tolist(), key="suggest_where")
                urgency = st.select_slider(t("urgency"), ["Nice to have", "Would help", "Needed", "Urgent"],
                                           format_func=opt, key="suggest_urgency")
                if st.form_submit_button(t("submit_suggestion"), use_container_width=True):
                    st.success(t("recorded_demo"))

        with col_reviews:
            st.subheader(t("community_ratings"))
            for r in RATINGS:
                stars = "⭐" * int(r["rating"])
                label = t("label_great") if r["rating"] >= 4 else t("label_ok") if r["rating"] >= 3 else t("label_avoid")
                comment = RATING_COMMENTS_DE.get(r["spot"], r["comment"]) if lang == "de" else r["comment"]
                st.markdown(f"**{r['spot']}** {stars} ({r['rating']}/5 · {r['reviews']} {t('reviews')})")
                st.caption(f'"{comment}" {label}')
                st.divider()

            st.subheader(t("most_requested"))
            fig = px.bar(
                pd.DataFrame({"Need": [opt(n) for n in ["Trees", "Fountains", "Benches", "Cooling", "Pet Water", "Sensors"]],
                              "Votes": [45, 38, 31, 22, 18, 15]}),
                x="Votes", y="Need", orientation="h", color="Votes",
                color_continuous_scale=["#c8e6c9", "#2e7d32"],
                labels={"Need": t("need"), "Votes": t("votes")}
            )
            fig.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # ─── Sub-tab: Community Ideas Board ───
    with ideas_tab:
        st.subheader(t("subtab_ideas"))
        st.write(t("ideas_intro"))

        # Post your idea form
        with st.expander(t("post_idea"), expanded=False):
            with st.form("idea_form"):
                idea_title = st.text_input(t("idea_title"), placeholder=t("idea_title_placeholder"), key="idea_title")
                idea_category = st.selectbox(t("category"),
                    ["Cooling Infrastructure", "Water & Drinking Fountains", "Sensor Network",
                     "Green Spaces", "Pet Friendly", "Accessibility", "Other"],
                    format_func=opt, key="idea_category")
                idea_location = st.selectbox(t("suggested_location"), SENSORS["name"].tolist(), key="idea_loc")
                idea_desc = st.text_area(t("describe_idea"), placeholder=t("describe_idea_placeholder"), key="idea_desc")
                idea_image = st.file_uploader(t("upload_photo"), type=["png", "jpg", "jpeg"], key="idea_image")
                if st.form_submit_button(t("post_idea_btn"), use_container_width=True):
                    st.success(t("idea_posted"))

        st.divider()

        # ─── Existing community ideas ───

        # IDEA 1: Cooling Wall
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🧊</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">{t('idea1_title')}</span>
                <span style="background: #2196f3; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">{opt('Cooling Infrastructure')}</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">{t('idea1_meta')}</p>
        </div>
        """, unsafe_allow_html=True)

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
            c1, c2, c3 = st.columns(3)
            c1.button(t("n_votes", n=47), key="vote_1", use_container_width=True)
            c2.button(t("n_comments", n=12), key="comment_1", use_container_width=True)
            c3.button(t("show_on_map"), key="map_1", use_container_width=True)

        st.divider()

        # IDEA 2: Lamp Post Sensors
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">📡</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">{t('idea2_title')}</span>
                <span style="background: #ff9800; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">{opt('Sensor Network')}</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">{t('idea2_meta')}</p>
        </div>
        """, unsafe_allow_html=True)

        col_img2, col_desc2 = st.columns([1, 2])
        with col_img2:
            lamp_img = "smart-lamp-post-de.svg" if lang == "de" else "smart-lamp-post.svg"
            try:
                st.image(str(IMAGES_DIR / lamp_img), use_container_width=True)
            except:
                st.info(t("image_missing", file=lamp_img))
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e65100, #ff9800); border-radius: 10px; padding: 1rem; text-align: center; color: white;">
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
            c1, c2, c3 = st.columns(3)
            c1.button(t("n_votes", n=63), key="vote_2", use_container_width=True)
            c2.button(t("n_comments", n=21), key="comment_2", use_container_width=True)
            c3.button(t("show_on_map"), key="map_2", use_container_width=True)

        st.divider()

        # IDEA 3: Pet-Friendly Water Stations
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🐕</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">{t('idea3_title')}</span>
                <span style="background: #4caf50; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">{opt('Pet Friendly')}</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">{t('idea3_meta')}</p>
        </div>
        """, unsafe_allow_html=True)

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
            c1, c2, c3 = st.columns(3)
            c1.button(t("n_votes", n=52), key="vote_3", use_container_width=True)
            c2.button(t("n_comments", n=18), key="comment_3", use_container_width=True)
            c3.button(t("show_on_map"), key="map_3", use_container_width=True)

        st.divider()

        # IDEA 4: Kids Tree Planting Initiative
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e8f5e9, #a5d6a7); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🌱</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">{t('idea4_title')}</span>
                <span style="background: #43a047; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">{opt('Kids Initiative')}</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">{t('idea4_meta')}</p>
        </div>
        """, unsafe_allow_html=True)

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
            c1, c2, c3 = st.columns(3)
            c1.button(t("n_votes", n=203), key="vote_4", use_container_width=True)
            c2.button(t("n_comments", n=67), key="comment_4", use_container_width=True)
            c3.button(t("show_on_map"), key="map_4", use_container_width=True)
            st.caption(t("idea4_top_comment"))

        st.divider()

        # IDEA 5: Elderly Crochet Shade Canopy
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fff8e1, #ffecb3); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🧶</span>
                <span style="font-weight: bold; font-size: 1.2rem; margin-left: 0.5rem; color: #111;">{t('idea5_title')}</span>
                <span style="background: #f9a825; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: auto;">{opt('Community Project')}</span>
            </div>
            <p style="color: #555; font-size: 0.85rem;">{t('idea5_meta')}</p>
        </div>
        """, unsafe_allow_html=True)

        col_img5, col_desc5 = st.columns([1, 2])
        with col_img5:
            try:
                st.image(str(IMAGES_DIR / "canopy-5.jpg"), use_container_width=True)
            except:
                st.info(t("image_missing", file="canopy-5.jpg"))
            st.caption(t("idea5_caption"))
        with col_desc5:
            st.markdown(t("idea5_body"))
            c1, c2, c3 = st.columns(3)
            c1.button(t("n_votes", n=112), key="vote_5", use_container_width=True)
            c2.button(t("n_comments", n=43), key="comment_5", use_container_width=True)
            c3.button(t("show_on_map"), key="map_5", use_container_width=True)
            st.caption(t("idea5_top_comment"))
