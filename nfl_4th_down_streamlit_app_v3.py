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
        max-width: 1320px;
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
    .guide-box {
        padding: 1rem 1.1rem;
        border-radius: 14px;
        background: rgba(59,130,246,.08);
        border: 1px solid rgba(59,130,246,.18);
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

PAGES = ["Home", "NFL 4th Down", "How to Use This App", "About"]

sample_lookup = pd.DataFrame(
    [
        [4, "Trailing", "61-80", "1-2", "Go For It", 0.81, "Short yardage while trailing in plus territory favors aggression."],
        [4, "Trailing", "41-60", "3-5", "Go For It", 0.71, "Late-game trailing spots often justify a higher-risk decision."],
        [4, "Tied", "61-80", "3-5", "Field Goal", 0.64, "A makeable kick range can make the field goal attractive in neutral late-game spots."],
        [3, "Leading", "21-40", "8+", "Punt", 0.77, "When leading and facing long yardage deep in your own side, field position becomes more valuable."],
        [2, "Tied", "61-80", "1-2", "Go For It", 0.74, "Short-yardage plus territory often increases conversion appeal even outside late-game moments."],
        [1, "Tied", "41-60", "8+", "Punt", 0.73, "Early-game long-yardage situations in middling field position often favor a punt."],
        [4, "Leading", "81-99", "3-5", "Field Goal", 0.69, "When already in likely kicking range while leading, the safer scoring option can dominate."],
    ],
    columns=["Quarter", "Game State", "Field Zone", "Distance Bucket", "Recommendation", "Confidence", "Rationale"],
)

with st.sidebar:
    st.markdown("## Will Escalante")
    st.caption("Interactive portfolio app")
    page = st.radio("Navigate", PAGES, index=1)
    st.divider()
    st.markdown("**Current featured project**")
    st.write("NFL 4th Down Win Probability Decision Tool")
    st.markdown("**Next build candidate**")
    st.write("Employee Attrition, Heart Disease, or Automatidata")
    st.divider()
    st.markdown("**Links**")
    st.markdown("[NFL Project Repo](https://github.com/imthepersona/nfl-4th-down-win-probability)")
    st.markdown("[LinkedIn](https://www.linkedin.com)")

def game_state_label(score_diff):
    if score_diff < 0:
        return "Trailing"
    if score_diff > 0:
        return "Leading"
    return "Tied"

def field_zone_label(yard_line):
    if yard_line <= 20:
        return "1-20"
    if yard_line <= 40:
        return "21-40"
    if yard_line <= 60:
        return "41-60"
    if yard_line <= 80:
        return "61-80"
    return "81-99"

def distance_bucket_label(yards_to_go):
    if yards_to_go <= 2:
        return "1-2"
    if yards_to_go <= 5:
        return "3-5"
    if yards_to_go <= 7:
        return "6-7"
    return "8+"

def recommendation_engine(quarter, yards_to_go, yard_line, score_diff):
    game_state = game_state_label(score_diff)
    field_zone = field_zone_label(yard_line)
    distance_bucket = distance_bucket_label(yards_to_go)

    match = sample_lookup[
        (sample_lookup["Quarter"] == quarter)
        & (sample_lookup["Game State"] == game_state)
        & (sample_lookup["Field Zone"] == field_zone)
        & (sample_lookup["Distance Bucket"] == distance_bucket)
    ]

    if not match.empty:
        row = match.iloc[0]
        return row["Recommendation"], row["Rationale"], float(row["Confidence"]), game_state, field_zone, distance_bucket, True

    if quarter == 4 and score_diff < 0 and yard_line >= 55 and yards_to_go <= 5:
        return "Go For It", "Late-game trailing context in plus territory usually calls for an aggressive decision.", 0.74, game_state, field_zone, distance_bucket, False
    if yard_line >= 70 and yards_to_go <= 6:
        return "Field Goal", "This area often supports a realistic field goal attempt if the kick unit is trusted.", 0.68, game_state, field_zone, distance_bucket, False
    if yards_to_go <= 2 and yard_line >= 60:
        return "Go For It", "Short-yardage situations across favorable field position often increase conversion appeal.", 0.79, game_state, field_zone, distance_bucket, False
    if yards_to_go >= 8 and yard_line <= 55:
        return "Punt", "Long-yardage situations backed up away from the goalposts usually favor field position.", 0.72, game_state, field_zone, distance_bucket, False
    return "Punt", "This fallback logic applies when no lookup row matches yet. Replace this with your trained model or larger recommendation table.", 0.58, game_state, field_zone, distance_bucket, False

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
        st.metric("Ready for demo", "Yes")

    st.write("")
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="project-card"><div class="section-label">Why Streamlit</div><strong>Better than static dashboards</strong><p style="margin-top:.5rem;">Use Streamlit when you want portfolio work to feel like a product: interactive controls, dynamic outputs, and a stronger client-facing experience.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="project-card"><div class="section-label">What changed in v3</div><strong>Visual + logic upgrades</strong><p style="margin-top:.5rem;">This version supports heatmap display, a sample recommendation lookup table, and a dedicated professional usage guide.</p></div>', unsafe_allow_html=True)

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
        st.caption("Replace these with your final validated project metrics if needed.")

    st.write("")
    st.markdown("### Scenario Explorer")
    st.caption("This version uses a sample lookup-table layer first, then falls back to rule-based prototype logic.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        quarter = st.selectbox("Quarter", [1, 2, 3, 4], index=3)
    with c2:
        yards_to_go = st.slider("Yards to go", 1, 15, 3)
    with c3:
        yard_line = st.slider("Yard line", 1, 99, 62)
    with c4:
        score_diff = st.slider("Score differential", -21, 21, -3)

    decision, explanation, confidence, game_state, field_zone, distance_bucket, used_lookup = recommendation_engine(
        quarter, yards_to_go, yard_line, score_diff
    )

    r1, r2 = st.columns([1.2, 1])
    with r1:
        st.markdown("### Model Recommendation")
        st.markdown(f'<div class="callout"><strong>{decision}</strong><br>{explanation}</div>', unsafe_allow_html=True)
        st.metric("Prototype confidence score", f"{confidence:.0%}")
        st.caption("This is currently a portfolio demo recommendation, not your final production model.")
    with r2:
        st.markdown("### Context Summary")
        summary_df = pd.DataFrame(
            {
                "Input": ["Quarter", "Yards to go", "Yard line", "Score differential", "Game state", "Field zone", "Distance bucket"],
                "Value": [quarter, yards_to_go, yard_line, score_diff, game_state, field_zone, distance_bucket],
            }
        )
        st.dataframe(summary_df, width="stretch", hide_index=True)

    if used_lookup:
        st.success("This recommendation matched a row in the sample lookup table. Later, you can replace this table with your real recommendation CSV.")
    else:
        st.warning("No lookup-table match was found for this exact scenario, so the app used fallback prototype logic.")

    st.write("")
    st.markdown("### Recommendation Logic Table")
    st.caption("This sample table shows the structure you can expand with your actual model outputs or recommendation matrix.")
    st.dataframe(sample_lookup, width="stretch", hide_index=True)

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
    st.markdown("### Heatmap Visual")
    st.caption("This heatmap is loaded from the repo for a cleaner public demo.")
    st.image(
        "Visualizations/images/Field Position x Distance Heatmap (1).png",
        caption="NFL 4th Down Tableau heatmap",
        width="stretch"
    )

    st.markdown("### Recommended next upgrades")
    st.markdown(
        """
- Replace the sample lookup table with your actual recommendation CSV or model output.
- Add class probabilities or win-probability change.
- Add a repo button, project summary PDF, and contact CTA.
- Add your second featured project as a new page.
        """
    )
    st.markdown('<div class="footer-note">This app is designed as a polished portfolio shell first, then a production-style analytics demo second.</div>', unsafe_allow_html=True)

elif page == "How to Use This App":
    st.markdown('<div class="section-label">Professional guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">How this Streamlit app works</div>', unsafe_allow_html=True)
    st.write(
        "This app is a professional portfolio demo that helps people explore your NFL 4th-down project through interactive controls, visuals, and recommendation output instead of just reading a notebook or README."
    )

    st.markdown("### What each page does")
    st.markdown(
        """
- **Home:** Introduces your portfolio app and highlights the featured project.
- **NFL 4th Down:** Lets users test scenarios, view recommendation output, inspect a sample logic table, and view your heatmap.
- **How to Use This App:** Explains the app's purpose and how to present it professionally.
- **About:** Gives context on your portfolio direction and where the app is headed.
        """
    )

    st.markdown("### How the recommendation section works")
    st.markdown(
        """
1. The user chooses quarter, yards to go, yard line, and score differential.
2. The app converts those inputs into simplified categories like game state, field zone, and distance bucket.
3. The app first checks a sample lookup table for a matching recommendation.
4. If no exact match exists, it falls back to prototype rule-based logic.
5. The app then displays a recommendation, rationale, and confidence score.
        """
    )

    st.markdown("### How to use it professionally")
    st.markdown(
        """
- Use it during interviews to show that you can move beyond notebooks into interactive analytics delivery.
- Use it in your portfolio as a live project companion to your GitHub repo and README.
- Use it with recruiters or hiring managers to walk through one or two scenarios and explain your decision logic.
- Use it with sports analytics audiences to show how your findings can be translated into a product-style tool.
- Use it as a bridge project before building a fuller production version with a saved model and cloud deployment.
        """
    )

    st.markdown("### Best professional workflow")
    st.markdown(
        """
- Keep the README for technical depth.
- Keep Tableau for polished static visuals.
- Use this Streamlit app for interactive storytelling and demonstration.
- Later deploy it publicly so people can test the project without running local code.
        """
    )

    st.markdown(
        '<div class="guide-box"><strong>Professional positioning tip:</strong><br>Talk about this app as a decision-support prototype that translates analysis into an interactive product experience. That framing sounds stronger than calling it just a dashboard.</div>',
        unsafe_allow_html=True,
    )

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
