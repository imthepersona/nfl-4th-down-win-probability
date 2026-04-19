# NFL 4th Down Decision Analysis

## 1. Project overview

This project analyzes NFL 4th-down situations and builds models to recommend whether an offense should **go for it**, attempt a **field goal**, or **punt**, given the game context.

Using historical play-by-play data from 2009–2018, the project creates a clean, labeled 4th-down dataset, engineers rich pre-snap features, and trains multiclass models to understand and predict 4th-down decision-making.

---

## 2. Repository structure

The repository follows a cookiecutter-style data science layout, with notebooks grouped by phase.

```text
nfl-4th-down-win-probability/
├── data/
│   ├── raw/           # Original Kaggle play-by-play CSV (not tracked in git)
│   ├── interim/       # Cleaned 4th-down subset(s)
│   └── processed/     # Feature-engineered datasets for modeling and analysis
├── notebooks/
│   ├── 01_cleaning_eda/
│   │   └── 01_4th_down_data_cleaning.ipynb
│   ├── 02_feature_engineering/
│   │   └── 02_4th_down_feature_engineering_eda.ipynb
│   └── 03_modeling/
│       └── 03_4th_down_modeling.ipynb
├── models/            # Trained model artifacts (optional, may be git-ignored)
├── reports/           # Figures, tables, and written summaries
├── src/               # (Optional) Reusable Python modules for pipeline steps
├── pyproject.toml or requirements.txt
└── README.md
```

- Cleaning & EDA notebooks live in `notebooks/01_cleaning_eda`.
- Feature engineering & EDA live in `notebooks/02_feature_engineering`.
- Modeling and evaluation live in `notebooks/03_modeling`.

---

## 3. Data

### 3.1 Source

- Dataset: NFL Play-by-Play Data 2009–2018 (Max Horowitz et al., Kaggle).
- Each row is a single play, with detailed game context, play description, and advanced metrics (e.g., expected points, EPA, touchdown and field goal probabilities).

> Note: The original Kaggle CSV is large and may not be tracked in this repo. To fully reproduce the pipeline, download the dataset from Kaggle and place the CSV under `data/raw/`.

### 3.2 Derived datasets

The notebooks create several project-specific datasets.

- `data/interim/fourth_down_scenarios.csv`  
  All 4th-down plays, filtered from the raw data with selected columns such as `game_id`, `play_id`, `qtr`, `yardline_100`, `ydstogo`, scores, time remaining, timeouts, EPA/EP, and decision/outcome flags.

- `data/processed/feature_df.csv`  
  Labeled and feature-engineered 4th-down plays, including:
  - Cleaned decision labels.
  - Engineered buckets (field position, distance, score, time, timeouts, quarter).
  - Binary flags (red zone, short yardage, overtime, late-game close).
  - Post-play outcomes (`fourth_down_success`) and game outcome (`winner`, `pos_team_win`) for analysis.

- `data/processed/modeling_df.csv`  
  Modeling-ready table containing only pre-snap features and the multiclass decision label (no future information to avoid leakage).

- `data/processed/analysis_df.csv`  
  Same as the modeling table, plus post-play and post-game outcomes for descriptive analysis and plotting.

---

## 4. Problem formulation

### 4.1 Objective

Estimate and analyze 4th-down decisions in the NFL by learning from historical plays, focusing on whether the offense **punted**, attempted a **field goal**, or **went for it**.

The project treats the problem primarily as multiclass classification (predicting what decision is taken given the game state), and then examines success rates and win outcomes conditional on those decisions.

### 4.2 Labels

- **Decision label:** `decision_4th_class` ∈ {`punt`, `field_goal`, `go_for_it`}  
  Derived using a combination of:
  - `punt_attempt`
  - `field_goal_attempt`
  - cleaned `play_type` (`play_type_clean`)
  - cleaned `field_goal_result` (`field_goal_result_clean`)

  Ambiguous plays labeled as `missing` are filtered out.

- **Encoded decision label:** `decision_4th_class_encoded`  
  Mapped as: `punt` → 0, `field_goal` → 1, `go_for_it` → 2.

- **Outcome label:** `fourth_down_success`  
  Binary flag:
  - 1 if the offense converts for a new set of downs (`fourth_down_converted` = 1), scores a touchdown (`touchdown` = 1), or makes a field goal (`field_goal_result_clean` = 'made').
  - 0 otherwise.

- **Game outcome (analysis only):**
  - `winner`: inferred home/away winner for each game from final scores.
  - `pos_team_win`: 1 if the 4th-down offense (`posteam`) won the game, 0 otherwise.

---

## 5. Methodology and notebooks

The workflow is structured into three main phases, each corresponding to a notebook folder.

### 5.1 Phase 1 – Cleaning & initial preparation

**Notebook:** `notebooks/01_cleaning_eda/01_4th_down_data_cleaning.ipynb`

- Load the raw Kaggle CSV with `low_memory=False` to avoid mixed-type warnings and ensure stable typing.
- Identify and keep a targeted subset of features relevant for 4th-down analysis, including game context (quarter, time remaining, scores, timeouts), field position (`yardline_100`, `side_of_field`), and advanced metrics (TD/FG probabilities, EP, EPA).
- Filter to 4th-down plays (`down == 4`) and build a clean `fourth_down_scenarios` DataFrame.
- Normalize column names (strip whitespace), inspect nulls and types, and save an interim 4th-down CSV to `data/interim/`.

### 5.2 Phase 2 – Labeling, feature engineering, and EDA

**Notebook:** `notebooks/02_feature_engineering/02_4th_down_feature_engineering_eda.ipynb`

Key steps:

1. **Text cleaning & decisions**  
   - Standardize play text fields (`play_type_clean`, `field_goal_result_clean`) to lower-case, stripped strings.
   - Define:
     - `is_punt`: based on `punt_attempt` or `play_type_clean == 'punt'`.
     - `is_field_goal`: based on `field_goal_attempt`, `play_type_clean == 'field_goal'`, or any valid `field_goal_result_clean` (`made`, `missed`, `blocked`).
     - `is_go_for_it`: plays that are not punts/field goals but are runs, passes, QB kneels/spikes, or have 4th-down conversion flags.
   - Combine these into `decision_4th_class` and its encoded version.

2. **Success and game outcome**  
   - Create `fourth_down_success` as defined above.
   - Determine final game scores and winners, and whether the offense eventually won (`pos_team_win`).

3. **Feature engineering**  
   - Field position buckets: `field_position_bucket` combining field zone (backed up / own territory / plus territory / scoring range) with distance buckets (e.g., `1_or_less`, `2_to_3`, `4_to_5`, `6_to_10`, `11_plus`).
   - Score context: `score_diff_bucket` (trailing/leading by one or multiple possessions, tied).
   - Time context: `time_bucket` (e.g., early game, mid game, late game based on seconds remaining).
   - Timeouts and quarter: offense/defense timeouts, `timeout_bucket`, and `quarter_bucket` (first half, third quarter, fourth quarter, overtime).
   - Binary flags: `is_red_zone`, `is_short_yardage`, `is_overtime`, `late_game_close`.

4. **Datasets for modeling and analysis**  
   - Construct:
     - `modeling_df`: `decision_4th_class` / encoded target + pre-snap features only (no future leakage).
     - `analysis_df`: modeling features plus `fourth_down_success`, `winner`, `pos_team_win`.
     - `viz_df`: full `feature_df` for flexible visualization.
   - Save all to `data/processed/`.

5. **Exploratory data analysis (EDA)**  
   - Visualize:
     - Distribution of decision types (punt / field goal / go for it).
     - Overall success vs. failure on 4th downs.
     - Success rate by decision type.
     - Decision mix by field position, yards to go, time buckets, and play type.
     - Failure rates by decision type and context (e.g., failed field goals vs. failed conversions).

### 5.3 Phase 3 – Modeling & evaluation

**Notebook:** `notebooks/03_modeling/03_4th_down_modeling.ipynb`

At a high level:

- Use `modeling_df` to train baseline and improved classifiers for `decision_4th_class`.
- Compare three model configurations:
  - **M1:** Baseline model (e.g., early experiments that highlight issues such as including IDs or leakage-prone features).
  - **M2:** Balanced model without IDs, using class weights to handle class imbalance and a fixed hyperparameter set.
  - **M3:** Final tuned XGBoost model without IDs, optimized for macro F1 across the three decision classes.
- Evaluate with appropriate train/validation/test splits and metrics (macro F1, accuracy, confusion matrices), and interpret feature importances.

---

## 6. Key findings

Some of the main football and modeling insights from the analysis:

- **Coaches are conservative overall:**  
  Punts make up the majority of 4th-down decisions (around 60%), with field goals and go-for-it attempts splitting the remainder.

- **4th downs are often "unsuccessful" under this definition:**  
  Roughly three-quarters of 4th-down plays are labeled unsuccessful (no conversion, no touchdown, no made field goal), reflecting the inherent difficulty and risk of these situations.

- **Context drives decisions strongly:**  
  Field position, yards to go, and score/time buckets all have clear patterns:  
  - Deep in own territory or with long-yardage to go → punts dominate.  
  - In scoring range or with short yardage (≤ 2 yards) → more field goals and go-for-it attempts.

- **Late-game and red zone behavior:**  
  In `late_game_close` situations (≤ 10 minutes left and within one possession), teams become more aggressive, especially when already in plus territory or the red zone.

- **Model insights:**  
  In the final tuned XGBoost model, features such as `is_red_zone`, `yardline_100`, and late-game time buckets emerge as important drivers of decision predictions, aligning with football intuition.

---

## 7. How to run this project

### 7.1 Prerequisites

- Python 3.x  
- Git and a working virtual environment setup are recommended.

### 7.2 Setup

From your terminal:

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/nfl-4th-down-win-probability.git
cd nfl-4th-down-win-probability

# 2. (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scriptsctivate

# 3. Install dependencies
pip install -r requirements.txt
# or, if using pyproject.toml / poetry / hatch:
# pip install .
```

### 7.3 Data

1. Download the NFL Play-by-Play 2009–2018 CSV from Kaggle and place it under:

   ```text
   data/raw/NFL Play by Play 2009-2018 (v5).csv
   ```

   (Ensure the filename matches what the cleaning notebook expects.)

2. The notebooks will create the interim and processed datasets under `data/interim/` and `data/processed/` as they run.

### 7.4 Notebook workflow

Run the notebooks in order:

1. `notebooks/01_cleaning_eda/01_4th_down_data_cleaning.ipynb`  
2. `notebooks/02_feature_engineering/02_4th_down_feature_engineering_eda.ipynb`  
3. `notebooks/03_modeling/03_4th_down_modeling.ipynb`  

This will reproduce the full pipeline from raw play-by-play data through feature engineering, EDA, and model training.

---

## 8. Limitations and next steps

### Limitations

- **Historical and static:**  
  The project uses historical data only; there is no live updating or deployment component. Recommendations are based on past seasons and may not fully reflect current strategies.

- **Label bias:**  
  The model largely learns what coaches did, not necessarily the mathematically optimal choice, since `decision_4th_class` is derived from actual decisions.

- **Unmodeled factors:**  
  Important real-world context such as weather, injuries, or playoff stakes is not explicitly modeled and could affect decisions.

### Possible extensions

- Compare model-based recommendations (e.g., based on expected points or win probability) to actual coaching decisions to quantify how conservative or aggressive teams are.
- Train separate models by era, team, or coach to study style differences in 4th-down strategy.
- Extend to a win-probability or value-based framework that directly optimizes expected game outcome rather than matching coach choices.

---

## 9. References

- Kaggle – NFL Play-by-Play Data 2009–2018.
- Standard resources on expected points (EP), expected points added (EPA), and 4th-down decision analytics from football analytics literature and community articles.
