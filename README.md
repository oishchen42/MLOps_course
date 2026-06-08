# Production Project: MLOps and Dagster

This repository collects LEVEL3 workshop artifacts and demonstrates a reproducible MLOps workflow using notebooks and a Dagster project for a bike rentals use case.

## What you'll learn

- Core data engineering: ingestion, cleaning, and hourly aggregation.
- Feature engineering: time-based lags and rolling statistics, weather and holiday joins.
- Modeling & evaluation: linear and histogram-gradient-boosting regression, RMSE/MAE/R2 reporting, and permutation feature importance.
- Orchestration: packaging the pipeline as Dagster assets and exposing model metadata for inspection.

## Notebooks

- All interactive steps and experiments live in the `notebook/` folder. Key notebooks:
	- `notebook/week1_titanic1.ipynb` — Titanic EDA
	- `notebook/week1_titanic2.ipynb` — Classification experiments
	- `notebook/week2_bikes1.ipynb` — Bike pipeline and feature engineering
    - `notebook/week3_model_training.ipynb` — Workflow with the different models: 'Linear Regression and HistGradientBoostingRegressor'

## Weekly breakdown

- **Week 1 — Classification & EDA**
	- Goals: exploratory data analysis, baseline classifiers, metric interpretation.
	- Artifacts: Titanic notebooks, basic preprocessing code.

- **Week 2 — Bike Data Pipeline & Feature Engineering**
	- Goals: ingest bike and weather data, aggregate hourly, join holidays, and produce time-window features.
	- Artifacts: data ingestion scripts, `mlops/week-2/data` CSVs, feature-engineered dataset in `dagster_w2_w3/src/bikes/defs`.

- **Week 3 — Modeling, Evaluation & Dagster**
	- Goals: train regression models, compute RMSE/MAE/R2, produce feature-importance reports, and wrap training as Dagster assets.
	- Artifacts: model assets in `dagster_w2_w3/src/bikes/defs` and evaluation metadata attached to Dagster outputs.

## Data sources

- Titanic dataset: [mlops/week-1/data/titanic.csv](mlops/week-1/data/titanic.csv)
- Bike rentals datasets: [mlops/week-2/data/direct_pickup_bike_rentals.csv](mlops/week-2/data/direct_pickup_bike_rentals.csv), [mlops/week-2/data/registered_bike_rentals.csv](mlops/week-2/data/registered_bike_rentals.csv), [mlops/week-2/data/weather.csv](mlops/week-2/data/weather.csv), [mlops/week-2/data/holidays.csv](mlops/week-2/data/holidays.csv)

## Dagster pipeline (bike rentals)

The Dagster project in [dagster_w2_w3/README.md](dagster_w2_w3/README.md) builds assets from the week-2 bike rental CSVs and produces a feature-engineered dataset. Asset definitions live in `dagster_w2_w3/src/bikes/defs/`.

### IMPORTANT:
* add to the root with this project mlops directory form the ARKADIA's LEVEL3 repository, as all the datasets are taken from there

### Run Dagster locally

```bash
cd bikes_dagster
# Option 1: uv
uv sync
source .venv/bin/activate
dg dev
```

Open http://localhost:3000 in your browser.

### Alternative: pip

```bash
cd bikes_dagster
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
dg dev
```



