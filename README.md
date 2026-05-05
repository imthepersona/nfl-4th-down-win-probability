# NFL 4th Down Decision Model

A machine learning project that analyzes NFL 4th-down situations and predicts the most likely decision: go for it, attempt a field goal, or punt based on game context.

## Project Overview

This repository explores 4th-down decision-making through predictive modeling and situational football analytics. The project uses historical NFL play-by-play data, feature engineering, and multi-class classification to evaluate how factors such as field position, yards to go, score differential, quarter, and time remaining influence 4th-down decisions.

The central question behind this project is:

**Given the current game situation, which 4th-down decision is most appropriate: go for it, kick a field goal, or punt?**

## Key Features

- **Multi-class classification** for 4th-down decision prediction.
- **Decision analysis** across go-for-it, field goal, and punt outcomes.
- **Feature engineering** for game context, field position, clock, and score margin.
- **Notebook-based workflow** for cleaning, exploration, feature engineering, and modeling.
- **Project artifacts** including saved models, reports, and visualizations.
- **Azure pipeline support** through `load_nfl_to_azure.py`.

## Data Sources

This project uses NFL play-by-play data sourced from Kaggle:

- [NFL Play by Play 2009-2016](https://www.kaggle.com/datasets/maxhorowitz/nflplaybyplay2009to2016)

Supporting project materials are organized across the repository, including:
- Data files and data dictionaries in `data/`.
- Analysis notebooks in `notebooks/`, including the subfolders `cleaning_eda/`, `feature_engineering/`, and `modeling/`.
- Saved model artifacts in `models/`.
- Supporting documents (reports and key visuals) in the `reports/` and `visualizations/` directories.

## Methods Summary

The project follows a structured sports analytics workflow:

1. Collect and prepare NFL play-level data.
2. Filter for relevant 4th-down situations.
3. Engineer game-state features tied to 4th-down decisions.
4. Train and tune classification models.
5. Evaluate performance using macro F1, accuracy, precision, and recall.
6. Summarize findings through notebooks, reports, and visualizations.

This project is focused on **decision prediction**, not on manually created probability features. Any probability estimates come from the trained model itself rather than from standalone probability-engineered inputs.

## Repository Structure

```text
.
├── data/                          # Data files and data dictionaries
├── docs/                          # Supporting project documentation
├── models/                        # Saved models and model-related outputs
├── references/                    # Supporting reference materials
├── reports/                       # Reports, summaries, and project outputs
├── tests/                         # Test files
├── visualizations/                # Charts and project visuals
├── notebooks/                     # Jupyter notebooks for project analysis
│   ├── cleaning_eda/              # Data cleaning and exploratory analysis
│   ├── feature_engineering/       # Feature creation and transformation
│   └── modeling/                  # Model training and evaluation
├── load_nfl_to_azure.py           # Data-loading utility
└── README.md
```

## Key Findings

### Coach behavior

- Coaches choose the conservative option most often, punting on approximately 60.8% of 4th downs, attempting field goals on 22.8%, and going for it on only 16.4% of plays in the dataset.
- Only 25.8% of 4th-down plays result in a successful outcome for the offense, defined as either scoring points or gaining a first down.
- Field goals succeed about 85% of the time, while go-for-it attempts succeed about 36.2% of the time.

### Typical decision patterns

- Field goal attempts are concentrated in the red zone and are more common when the offense faces longer distances to go. 
- Punts mostly occur in the offense’s own territory, across a wide range of yards-to-go situations. 
- Go-for-it attempts cluster in opponent territory, usually with 1 yard or less to go and more often earlier than later in the game. 

## Results Highlights

The final model is **`xgb_4th_down_decision_balanced`**, an XGBoost classifier tuned to predict 4th-down decisions across three classes.

### Final model performance

- **Best parameters:** `{'colsample_bytree': 0.9, 'gamma': 0, 'max_depth': 4, 'min_child_weight': 3, 'subsample': 0.9}` 
- **Best CV macro F1:** `0.8382`
- **Test accuracy:** `0.8857` 

### Classification report

| Class | Precision | Recall | F1-score | Support |
|------|----------:|-------:|---------:|--------:|
| 0 | 0.948 | 0.933 | 0.941 | 4784 |
| 1 | 0.883 | 0.905 | 0.894 | 1794 |
| 2 | 0.667 | 0.683 | 0.675 | 1290 |
| Macro Avg | 0.833 | 0.840 | 0.836 | 7868 |
| Weighted Avg | 0.887 | 0.886 | 0.886 | 7868 |

### Key takeaway

The tuned XGBoost model performed strongly overall, with the best results on the majority classes and weaker but usable performance on the third class. This indicates that the model captures meaningful 4th-down decision patterns from game-state variables while still reflecting the inherent imbalance and complexity of real coaching behavior.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/imthepersona/nfl-4th-down-win-probability.git
cd nfl-4th-down-win-probability
pip install -r requirements.txt
```

If you prefer a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

For Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

### Run notebooks

```bash
jupyter notebook
```

Then open the notebooks in `notebooks/` to review cleaning, exploratory analysis, feature engineering, modeling, and evaluation.

### Load NFL data to Azure

A utility script is included for cloud data loading:

```bash
python load_nfl_to_azure.py
```

Update environment variables, credentials, and connection settings before running this script.

## Streamlit App

This project includes a Streamlit app that turns the NFL 4th-down analysis into an interactive decision-support demo.

### What the app does
- Lets users select quarter, yards to go, yard line, and score differential.
- Builds a pre-snap feature row that matches the trained model input structure.
- Uses a saved multi-class XGBoost model to estimate the best 4th-down decision.
- Shows the top recommendation and probability breakdown for Punt, Field Goal, and Go For It.
- Includes historical context and supporting visualizations.

### Run locally
From the project root:

```bash
python3 -m streamlit run nfl_4th_down_streamlit_app_v3.py
```

### Deployment
This app is designed for Streamlit Community Cloud deployment.

Required files:
- `nfl_4th_down_streamlit_app_v3.py`
- `requirements.txt`
- `models/xgb_4th_down_decision_balanced.pkl`
- `visualizations/images/field_position_distance_heatmap.png`

### Live app
Add your deployed app URL here once published.

Example:
`https://your-app-name.streamlit.app`

## Contributing

Contributions are welcome.

If you would like to improve the project:
- Open an issue to discuss a bug, enhancement, or research idea.
- Submit a pull request with clear notes on the change.
- Keep notebook outputs clean and document major modeling changes.
- Add tests when introducing reusable code or pipeline updates.

Recommended contribution areas:
- model evaluation improvements,
- feature engineering enhancements,
- visualization polish,
- reproducibility and environment setup,
- documentation clarity.

## Notes

This README is intentionally concise and designed for a portfolio-style analytics repository. For deeper detail, review the notebooks, reports, model artifacts, and supporting documentation included in the project. 