# Task Round Submission — AI Innovators Hub Project Selection

This repository contains submissions for **Track A (Data Analyst)** and **Track B (ML Engineer)**, both built on the Bank Marketing Dataset. Each track lives in its own folder.

---

## Repository Structure

```
├── task1/                        ← Track A: Data Analyst
│   ├── bank-full.csv
│   ├── Track1.ipynb              ← EDA notebook
│   └── Streamlit_Dashboard.py   ← Interactive dashboard
│
└── task2/                        ← Track B: ML Engineer
    ├── bank-full.csv
    ├── Track2.ipynb              ← ML pipeline notebook
    └── report.html               ← Auto-generated profiling report
```

---

## Dataset

Both tracks use the **Bank Marketing Dataset** (`bank-full.csv`) — data from direct phone marketing campaigns of a Portuguese bank. The target column `y` indicates whether a customer subscribed to a term deposit (`yes` / `no`).

> The CSV uses **semicolons (`;`)** as its delimiter. Both notebooks and the dashboard handle this automatically.

---

## Track A — Data Analyst (`task1/`)

### What this track covers

1. Loading the data and understanding it — shape, dtypes, missing values, class distribution
2. Answering four business questions with plots:
   - Which job types have the highest subscription rate?
   - Is there a pattern between account balance and likelihood to subscribe?
   - How does subscription rate differ across age groups? (binned: 18–30, 31–45, 46–60, 60+)
   - Does having an existing housing loan make someone less likely to take a new product?
3. A Streamlit dashboard surfacing these insights interactively for a bank relationship manager

### Prerequisites

```bash
pip install streamlit pandas plotly matplotlib seaborn jupyter
```

### Running the EDA Notebook

```bash
cd task1
jupyter notebook Track1.ipynb
```

Run cells top to bottom. The notebook walks through each of the four business questions with supporting plots and written observations.

### Running the Streamlit Dashboard

The dashboard expects `bank-full.csv` to be in the **same directory** as `Streamlit_Dashboard.py`.

```bash
cd task1
streamlit run Streamlit_Dashboard.py
```

The app opens automatically at `http://localhost:8501`.

### Dashboard Features

**Sidebar filters** (apply across all tabs):
- Job type (multi-select)
- Housing loan status
- Age range (slider)

**Live KPI cards** — update with every filter change:
- Total customers
- Total subscribers
- Subscription rate
- Average account balance

**Five analysis tabs:**

| Tab | What it shows |
|---|---|
| Job Analysis | Subscription rate by job category |
| Balance Analysis | Subscription rate across balance buckets (adjustable bin count) |
| Age Analysis | Subscription rate across the four age groups |
| Housing Loan | Subscription rate split by housing loan status |
| Data Explorer | Browse the filtered data + download as CSV |

---

## Track B — ML Engineer (`task2/`)

### What this track covers

1. Focused EDA — class distribution, encoding categoricals, handling missing values
2. Two models trained and compared:
   - **Baseline:** Logistic Regression
   - **Main model:** CatBoost Classifier
3. Proper evaluation — accuracy, precision, recall, F1, and full `classification_report` for both
4. 5 customer predictions from the test set (at least 2 predicted "yes", 2 predicted "no") with features, prediction, and probability score
5. Saved model file (`model.pkl`)

### Prerequisites

```bash
pip install pandas scikit-learn catboost joblib jupyter ydata-profiling
```

> **Note:** The `report.html` profiling report is already pre-generated and included. The profiling cell in the notebook is commented out — you don't need to re-run it.

### Running the Notebook

```bash
cd task2
jupyter notebook Track2.ipynb
```

Run cells sequentially. Here's what each stage does:

| Stage | Details |
|---|---|
| Data loading | Reads `bank-full.csv` with semicolon delimiter |
| Train/test split | 80/20, `random_state=21` |
| Preprocessing | Numerical → StandardScaler · Ordinal (education, month) → OrdinalEncoder · Nominal → OneHotEncoder · Combined via `ColumnTransformer` |
| Baseline model | Logistic Regression + `classification_report` |
| Main model | CatBoost — handles categoricals natively, no manual encoding needed |
| Sample predictions | 5 customers from test set with features, predicted label, and probability |
| Model export | Saves trained CatBoost model as `model.pkl` via `joblib` |

### Viewing the Profiling Report

`report.html` is a standalone file — no server needed. Open it directly:

```bash
# macOS
open task2/report.html

# Linux
xdg-open task2/report.html

# Windows
start task2/report.html
```

Or just double-click it in your file explorer.

### Saved Model

The trained CatBoost model is exported as `model.pkl`. To load and use it elsewhere:

```python
import joblib
model = joblib.load("model.pkl")
predictions = model.predict(X_new)
probabilities = model.predict_proba(X_new)
```

---

## Tech Stack

| Library | Used in | Purpose |
|---|---|---|
| Pandas | Both | Data loading and manipulation |
| Matplotlib / Seaborn | Track A | EDA plots in notebook |
| Plotly | Track A | Interactive dashboard charts |
| Streamlit | Track A | Web dashboard |
| Scikit-learn | Track B | Preprocessing pipelines + Logistic Regression |
| CatBoost | Track B | Main classification model |
| Joblib | Track B | Model serialization |
| ydata-profiling | Track B | Automated EDA report |
