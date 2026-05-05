import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

st.set_page_config(page_title="NFL 4th Down Decision App", layout="wide")

# =========================================================
# Paths
# =========================================================
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

MODEL_PATH = PROJECT_ROOT / "models" / "xgb_4th_down_decision_balanced.pkl"
META_PATH = PROJECT_ROOT / "models" / "xgb_4th_down_metadata_balanced.pkl"

# =========================================================
# Load model + metadata
# =========================================================
@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    metadata = joblib.load(META_PATH)
    return model, metadata

model, metadata = load_artifacts()
feature_columns = metadata["feature_columns"]

DECISION_MAP = {
    0: "Punt",
    1: "Field Goal",
    2: "Go For It",
}

# =========================================================
# Model-schema-aligned feature engineering
# =========================================================
def bucket_field_position(yardline_100: float, ydstogo: int) -> str:
    y = float(yardline_100)
    togo = int(ydstogo)

    if y > 80:
        zone = "backed_up"
    elif y > 50:
        zone = "own_territory"
    elif y > 20:
        zone = "plus_territory"
    else:
        zone = "scoring_range"

    if togo <= 1:
        dist = "1_or_less"
    elif togo <= 3:
        dist = "2_to_3"
    elif togo <= 5:
        dist = "4_to_5"
    elif togo <= 10:
        dist = "6_to_10"
    else:
        dist = "11_plus"

    return f"{zone}__{dist}"


def bucket_score_diff(score_differential: float) -> str:
    x = float(score_differential)

    if x <= -9:
        return "trailing_2plus_possessions"
    elif -8 <= x <= -1:
        return "trailing_1_possession"
    elif x == 0:
        return "tied"
    elif 1 <= x <= 8:
        return "leading_1_possession"
    else:
        return "leading_2plus_possessions"


def bucket_time(game_seconds_remaining: float) -> str:
    seconds_left = float(game_seconds_remaining)

    if seconds_left > 1800:
        return "early_game"
    elif seconds_left > 600:
        return "mid_game"
    else:
        return "late_game"


def bucket_timeouts(pos_timeouts_remaining: int) -> str:
    x = int(pos_timeouts_remaining)

    if x == 0:
        return "no_timeouts"
    elif x == 1:
        return "one_timeout"
    elif x == 2:
        return "two_timeouts"
    else:
        return "three_timeouts"


def bucket_quarter(qtr: int) -> str:
    q = int(qtr)

    if q in [1, 2]:
        return "first_half"
    elif q == 3:
        return "third_quarter"
    elif q == 4:
        return "fourth_quarter"
    else:
        return "overtime"


def build_raw_feature_row(
    yardline_100,
    ydstogo,
    score_differential,
    game_seconds_remaining,
    qtr,
    pos_timeouts_remaining,
    def_timeouts_remaining,
):
    yardline_100 = float(yardline_100)
    ydstogo = int(ydstogo)
    score_differential = float(score_differential)
    game_seconds_remaining = float(game_seconds_remaining)
    qtr = int(qtr)
    pos_timeouts_remaining = int(pos_timeouts_remaining)
    def_timeouts_remaining = int(def_timeouts_remaining)

    row = {
        "yardline_100": yardline_100,
        "ydstogo": ydstogo,
        "score_differential": score_differential,
        "game_seconds_remaining": game_seconds_remaining,
        "qtr": qtr,
        "pos_timeouts_remaining": float(pos_timeouts_remaining),
        "def_timeouts_remaining": float(def_timeouts_remaining),
        "is_red_zone": int(yardline_100 <= 20),
        "is_short_yardage": int(ydstogo <= 2),
        "is_overtime": int(qtr > 4),
        "late_game_close": int(
            (game_seconds_remaining <= 600) and (-8 <= score_differential <= 8)
        ),
        "field_position_bucket": bucket_field_position(yardline_100, ydstogo),
        "score_diff_bucket": bucket_score_diff(score_differential),
        "time_bucket": bucket_time(game_seconds_remaining),
        "timeout_bucket": bucket_timeouts(pos_timeouts_remaining),
        "quarter_bucket": bucket_quarter(qtr),
    }

    return pd.DataFrame([row])


def encode_and_align_features(raw_row: pd.DataFrame) -> pd.DataFrame:
    categorical_cols = [
        "field_position_bucket",
        "score_diff_bucket",
        "time_bucket",
        "timeout_bucket",
        "quarter_bucket",
    ]

    feature_row = pd.get_dummies(raw_row, columns=categorical_cols, dtype=int)

    for col in feature_columns:
        if col not in feature_row.columns:
            feature_row[col] = 0

    extra_cols = [col for col in feature_row.columns if col not in feature_columns]
    if extra_cols:
        feature_row = feature_row.drop(columns=extra_cols)

    feature_row = feature_row[feature_columns]
    return feature_row


def derive_feature_row(
    yardline_100,
    ydstogo,
    score_differential,
    game_seconds_remaining,
    qtr,
    pos_timeouts_remaining,
    def_timeouts_remaining,
):
    raw_row = build_raw_feature_row(
        yardline_100=yardline_100,
        ydstogo=ydstogo,
        score_differential=score_differential,
        game_seconds_remaining=game_seconds_remaining,
        qtr=qtr,
        pos_timeouts_remaining=pos_timeouts_remaining,
        def_timeouts_remaining=def_timeouts_remaining,
    )
    feature_row = encode_and_align_features(raw_row)
    return raw_row, feature_row


def model_recommendation(
    yardline_100,
    ydstogo,
    score_differential,
    game_seconds_remaining,
    qtr,
    pos_timeouts_remaining,
    def_timeouts_remaining,
):
    raw_row, feature_row = derive_feature_row(
        yardline_100=yardline_100,
        ydstogo=ydstogo,
        score_differential=score_differential,
        game_seconds_remaining=game_seconds_remaining,
        qtr=qtr,
        pos_timeouts_remaining=pos_timeouts_remaining,
        def_timeouts_remaining=def_timeouts_remaining,
    )

    pred_probs = model.predict_proba(feature_row)[0]
    pred_class = int(np.argmax(pred_probs))
    best_action = DECISION_MAP[pred_class]
    best_conf = float(pred_probs[pred_class])

    comparison_df = pd.DataFrame(
        {
            "Decision": ["Punt", "Field Goal", "Go For It"],
            "Probability": pred_probs,
        }
    ).sort_values("Probability", ascending=False).reset_index(drop=True)

    explanation_parts = []

    if yardline_100 <= 20:
        explanation_parts.append("you are in the red zone")
    elif yardline_100 <= 50:
        explanation_parts.append("you are in plus territory")
    elif yardline_100 > 80:
        explanation_parts.append("you are backed up deep in your own territory")

    if ydstogo <= 2:
        explanation_parts.append("it is short yardage")
    elif ydstogo >= 10:
        explanation_parts.append("it is a long conversion distance")

    if qtr > 4:
        explanation_parts.append("the game is in overtime")
    elif game_seconds_remaining <= 600:
        explanation_parts.append("it is late in the game")

    if abs(score_differential) <= 8:
        explanation_parts.append("the score is within one possession")
    elif score_differential < -8:
        explanation_parts.append("the offense is trailing by multiple scores")
    elif score_differential > 8:
        explanation_parts.append("the offense is leading by multiple scores")

    if explanation_parts:
        explanation = (
            f"Recommended action: {best_action}. "
            + "This recommendation is influenced by the fact that "
            + ", ".join(explanation_parts)
            + "."
        )
    else:
        explanation = f"Recommended action: {best_action}."

    return best_action, explanation, best_conf, comparison_df, raw_row, feature_row


def format_game_clock(game_seconds_remaining: float) -> str:
    total = int(game_seconds_remaining)

    if total < 0:
        total = 0

    if total > 2700:
        qtr = 1
        time_left_in_qtr = total - 2700
    elif total > 1800:
        qtr = 2
        time_left_in_qtr = total - 1800
    elif total > 900:
        qtr = 3
        time_left_in_qtr = total - 900
    else:
        qtr = 4
        time_left_in_qtr = total

    minutes = int(time_left_in_qtr // 60)
    seconds = int(time_left_in_qtr % 60)

    return f"Q{qtr} - {minutes:02d}:{seconds:02d}"


# =========================================================
# App layout
# =========================================================
st.title("NFL 4th Down Decision Recommender")
st.markdown(
    "Use pre-snap game context to estimate whether the model would recommend a **Punt**, **Field Goal**, or **Go For It**."
)

page = st.sidebar.radio("Navigate", ["Home", "NFL 4th Down"])

if page == "Home":
    st.header("Home")
    st.write(
        "This app uses your final balanced XGBoost 4th-down classifier trained on pre-snap context only."
    )
    st.write(
        "The model uses engineered situational features such as field position, score context, time context, timeouts, red zone status, short-yardage status, overtime, and late-game close situations."
    )

elif page == "NFL 4th Down":
    st.header("NFL 4th Down Decision Tool")

    col1, col2 = st.columns(2)

    with col1:
        yardline_100 = st.slider(
            "Yards to opponent end zone",
            min_value=1,
            max_value=99,
            value=45,
            help="20 or less is red zone. Lower values mean closer to the opponent end zone.",
        )

        ydstogo = st.slider(
            "Yards to go",
            min_value=1,
            max_value=25,
            value=4,
        )

        score_differential = st.slider(
            "Score differential (offense - defense)",
            min_value=-35,
            max_value=35,
            value=0,
        )

        qtr = st.selectbox(
            "Quarter",
            options=[1, 2, 3, 4, 5],
            index=3,
            help="Use 5 for overtime.",
        )

    with col2:
        game_seconds_remaining = st.slider(
            "Game seconds remaining",
            min_value=0,
            max_value=3600,
            value=600,
            help="3600 = start of game, 0 = end of regulation.",
        )

        pos_timeouts_remaining = st.selectbox(
            "Offense timeouts remaining",
            options=[0, 1, 2, 3],
            index=2,
        )

        def_timeouts_remaining = st.selectbox(
            "Defense timeouts remaining",
            options=[0, 1, 2, 3],
            index=2,
        )

    st.caption(f"Clock context: {format_game_clock(game_seconds_remaining)}")

    if st.button("Get recommendation", type="primary"):
        try:
            (
                best_action,
                explanation,
                best_conf,
                comparison_df,
                raw_row,
                feature_row,
            ) = model_recommendation(
                yardline_100=yardline_100,
                ydstogo=ydstogo,
                score_differential=score_differential,
                game_seconds_remaining=game_seconds_remaining,
                qtr=qtr,
                pos_timeouts_remaining=pos_timeouts_remaining,
                def_timeouts_remaining=def_timeouts_remaining,
            )

            st.subheader(f"Recommended Decision: {best_action}")
            st.metric("Model confidence", f"{best_conf:.1%}")
            st.write(explanation)

            st.subheader("Decision probabilities")
            show_df = comparison_df.copy()
            show_df["Probability"] = show_df["Probability"].map(lambda x: f"{x:.1%}")
            st.dataframe(show_df, use_container_width=True, hide_index=True)

            st.subheader("Raw engineered feature row")
            st.dataframe(raw_row, use_container_width=True)

            st.subheader("Encoded feature row sent to model")
            st.dataframe(feature_row, use_container_width=True)

            st.subheader("Quick situational summary")
            st.write(f"- Field position bucket: **{raw_row.loc[0, 'field_position_bucket']}**")
            st.write(f"- Score bucket: **{raw_row.loc[0, 'score_diff_bucket']}**")
            st.write(f"- Time bucket: **{raw_row.loc[0, 'time_bucket']}**")
            st.write(f"- Timeout bucket: **{raw_row.loc[0, 'timeout_bucket']}**")
            st.write(f"- Quarter bucket: **{raw_row.loc[0, 'quarter_bucket']}**")
            st.write(f"- Red zone: **{bool(raw_row.loc[0, 'is_red_zone'])}**")
            st.write(f"- Short yardage: **{bool(raw_row.loc[0, 'is_short_yardage'])}**")
            st.write(f"- Overtime: **{bool(raw_row.loc[0, 'is_overtime'])}**")
            st.write(f"- Late game close: **{bool(raw_row.loc[0, 'late_game_close'])}**")

        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.write("Saved model feature columns:")
            st.write(feature_columns)