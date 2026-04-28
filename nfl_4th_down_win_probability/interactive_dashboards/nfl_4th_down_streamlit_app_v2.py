import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Will Escalante | NFL 4th Down App",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 0.25rem;
    }
    .subtle {
        color: #94a3b8;
        font-size: 0.98rem;
    }
    .section-label {
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .hero-card {
        padding: 1.35rem 1.4rem;
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(15,23,42,.96), rgba(30,41,59,.96));
        border: 1px solid rgba(148,163,184,.18);
        box-shadow: 0 12px 30px rgba(2,6,23,.18);
    }
    .insight-card {
        padding: 1.1rem 1.2rem;
        border-radius: 16px;
        background: rgba(15,23,42,.06);
        border: 1px solid rgba(148,163,184,.18);
        min-height: 160px;
    }
    .project-card {
        padding: 1.1rem 1.2rem;
        border-radius: 16px;
        background: rgba(15,23,42,.04);
        border: 1px solid rgba(148,163,184,.16);
    }
    .callout {
        padding: 1rem 1.1rem;
        border-left: 4px solid #22c55e;
        background: rgba(34,197,94,.08);
        border-radius: 10px;
        margin: 0.75rem 0 0.25rem 0;
    }
    .footer-note {
        color: #64748b;
        font-size: 0.88rem;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGES = ["Home", "NFL 4th Down", "About"]

with st.sidebar:
    st.markdown("## Will Escalante")
    st.caption("Interactive portfolio app")
    page = st.radio("Navigate", PAGES, index=1)
    st.divider()
    st.markdown("**Current featured project**")
    st.write("NFL 4th Down Win Probability Decision Tool")
    st.markdown("**Planned second project**")
    st.write("Employee Attrition, Heart Disease, or Automatidata")
    st.divider()
    st.markdown("**Links**")
    st.markdown("[NFL Project Repo](https://github.com/imthepersona/nfl-4th-down-win-probability)")
    st.markdown("[LinkedIn](https://www.linkedin.com)")

def recommendation_engine(quarter, yards_to_go, yard_line, score_diff):
    if quarter == 4 and score_diff < 0 and yard_line >= 55 and yards_to_go <= 5:
        return "Go For It", "Late-game trailing context in plus territory usually calls for an aggressive decision.", 0.74
    if yard_line >= 70 and yards_to_go <= 6:
        return "Field Goal", "This area often supports a realistic field goal attempt if the kick unit is trusted.", 0.68
    if yards_to_go <= 2 and yard_line >= 60:
        return "Go For It", "Short-yardage situations across favorable field position often increase conversion appeal.", 0.79
    if yards_to_go >= 8 and yard_line <= 55:
        return "Punt", "Long-yardage situations backed up away from the goalposts usually favor field position.", 0.72
    return "Punt", "This default placeholder logic should be replaced with your trained model or lookup table.", 0.58

if page == "Home":
    st.markdown('<div class="section-label">Portfolio app</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Analytics projects built to be explored, not just viewed.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtle">This Streamlit portfolio is designed to turn your case studies into interactive experiences for recruiters, hiring managers, and clients.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown(
            """
            <div class="hero-card">
                <div class="section-label">Featured build</div>
                <h3 style="margin:0 0 .35rem 0;">NFL 4th Down Win Probability Decision Tool</h3>
                <p style="margin:0; color:#cbd5e1;">
                A sports analytics case study built from public NFL play-by-play data to evaluate whether teams should punt,
                attempt a field goal, or go for it on 4th down.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.metric("Projects completed", "4")
        st.metric("Featured now", "1")
        st.metric("Next build target", "Project 2")

    st.write("")
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="project-card"><div class="section-label">Why Streamlit</div><strong>Better than static dashboards</strong><p style="margin-top:.5rem;">Use Streamlit when you want portfolio work to feel like a product: interactive controls, dynamic outputs, and a stronger client-facing experience.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="project-card"><div class="section-label">How to use this app</div><strong>Start with the NFL project</strong><p style="margin-top:.5rem;">Use the sidebar to open the NFL project page, explore a sample scenario, and later plug in your saved model, visuals, and business recommendations.</p></div>', unsafe_allow_html=True)

elif page == "NFL 4th Down":
    st.markdown('<div class="section-label">Sports analytics case study</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">NFL 4th Down Decision Tool</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtle">Interactive prototype for exploring 4th-down decisions using quarter, field position, yards to go, and score differential.</div>',
        unsafe_allow_html=True,
    )

    st.write("")
    top1, top2 = st.columns([1.7, 1])
    with top1:
        st.markdown(
            """
            <div class="hero-card">
                <div class="section-label">Project overview</div>
                <h3 style="margin:0 0 .45rem 0;">What should a coach do on 4th down?</h3>
                <p style="margin:0; color:#cbd5e1;">
                This project uses NFL play-by-play data to analyze coaching choices and create a foundation for a recommendation tool that can
                compare punt, field goal, and go-for-it decisions based on game context.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top2:
        st.markdown("### Key metrics")
        k1, k2, k3 = st.columns(3)
        k1.metric("Punt", "60.8%")
        k2.metric("FG", "22.8%")
        k3.metric("Go", "16.4%")
        st.caption("Use your final validated project metrics here.")

    st.write("")
    st.markdown("### Scenario Explorer")
    st.caption("This version uses portfolio-friendly placeholder logic so you can stand up the app quickly before wiring in your trained model.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        quarter = st.selectbox("Quarter", [1, 2, 3, 4, "OT"], index=3)
    with c2:
        yards_to_go = st.slider("Yards to go", 1, 15, 3)
    with c3:
        yard_line = st.slider("Yard line", 1, 99, 62)
    with c4:
        score_diff = st.slider("Score differential", -21, 21, -3)

    decision, explanation, confidence = recommendation_engine(quarter, yards_to_go, yard_line, score_diff)

    r1, r2 = st.columns([1.2, 1])
    with r1:
        st.markdown("### Model Recommendation")
        st.markdown(f'<div class="callout"><strong>{decision}</strong><br>{explanation}</div>', unsafe_allow_html=True)
        st.metric("Prototype confidence score", f"{confidence:.0%}")
        st.caption("Later, replace this with class probabilities or win-probability delta from your actual model.")
    with r2:
        st.markdown("### Context Summary")
        summary_df = pd.DataFrame(
            {
                "Input": ["Quarter", "Yards to go", "Yard line", "Score differential"],
                "Value": [quarter, yards_to_go, yard_line, score_diff],
            }
        )
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.write("")
    st.markdown("### Important Insights")
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown('<div class="insight-card"><div class="section-label">Coach behavior</div><strong>Most coaches still punt.</strong><p style="margin-top:.55rem;">About 60.8% of 4th-down situations in your current analysis end in a punt, which shows how conservative decision-making still is.</p></div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div class="insight-card"><div class="section-label">Aggression gap</div><strong>Going for it is still rare.</strong><p style="margin-top:.55rem;">Only about 16.4% of situations become go-for-it decisions, leaving room to compare human behavior against model-driven recommendations.</p></div>', unsafe_allow_html=True)
    with i3:
        st.markdown('<div class="insight-card"><div class="section-label">Visualization</div><strong>Heatmaps make the story clearer.</strong><p style="margin-top:.55rem;">Your Tableau work can show where go-for-it success changes by field position and yards to go, making the findings easier to interpret for non-technical viewers.</p></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### Decision Mix")
    decision_df = pd.DataFrame(
        {
            "Decision": ["Punt", "Field Goal", "Go For It"],
            "Rate": [60.8, 22.8, 16.4],
        }
    ).set_index("Decision")
    st.bar_chart(decision_df)

    st.write("")
    st.markdown("### Visual Section")
    st.info(
        "Add your Tableau heatmap export here with something like: `st.image('assets/heatmap.png', caption='Go-for-it success rate by field position and yards to go', use_container_width=True)`"
    )

    st.markdown("### Recommended next upgrades")
    st.markdown(
        """
- Connect your trained model or saved lookup table.
- Add class probabilities or win-probability change.
- Embed your Tableau heatmap and recommendation matrix exports.
- Add a repo button, project summary PDF, and contact CTA.
- Add your second featured project as a new page.
        """
    )
    st.markdown('<div class="footer-note">This app is designed as a polished portfolio shell first, then a production-style analytics demo second.</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="section-label">About</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">About this portfolio app</div>', unsafe_allow_html=True)
    st.write(
        "This app is meant to showcase analytics work in a more modern, interactive format than a static dashboard or GitHub README. "
        "The goal is to help clients and hiring managers quickly understand the project, the logic, and the insight."
    )
    st.markdown("### What this app should become")
    st.markdown(
        """
- A two-project Streamlit portfolio app.
- One featured sports analytics case study.
- One featured business analytics or machine learning case study.
- Shared branding, cleaner navigation, and downloadable supporting material.
        """
    )
