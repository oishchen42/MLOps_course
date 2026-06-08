# bikes (Dagster W2/W3)

This Dagster project contains the Week-2 data pipeline and Week-3 model training assets for the bike rentals exercise.

## Quick start

1. Install dependencies (either `uv` or `pip` as you prefer).

Option: `uv`

```bash
uv sync
source .venv/bin/activate
```

Option: `pip`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Start Dagster UI:

```bash
dg dev
```

Open http://localhost:3000 to inspect and materialize assets.

## What this project includes (Week 2 & 3)

- Data ingestion and cleaning assets (raw -> cleaned): `direct_pickup_bike_rentals`, `registered_bike_rentals`, `weather`, `holidays`.
- Merge and aggregation assets: `united_bike_rentals`, `merged_bikes_with_holidays`, `dfs_united_with_time_features`.
- Model-training assets:
	- `base_linear_model` — trains a linear regression model and returns model + scaler with evaluation metadata.
	- `advanced_tree_model` — trains a HistGradientBoostingRegressor and returns the model with evaluation metadata.

Each model asset returns metadata keys (`RMSE`, `MAE`, `R2_Score`) and a markdown table of feature importances.

## Notebooks (reference)

- `notebook/week2_bikes1.ipynb` — data pipeline walkthrough: ingestion, cleaning, hourly aggregation, joins, and feature engineering.
- `notebook/week3_model_training.ipynb` — model training experiments and local evaluation used to iterate on model code.

## How to run and inspect model assets

1. Start Dagster UI (`dg dev`) and open the project.
2. In the Assets view, locate the asset (e.g. `base_linear_model` or `advanced_tree_model`).
3. Materialize the asset to run the upstream pipeline; after completion, click the asset to view metadata and logs — model metrics and the feature importance markdown table are attached to the output.

## Notes

- The feature-engineered dataset `dfs_united_with_time_features` is produced in `src/bikes/defs/united_all.py` and used as input to model assets.
- Small code-doc updates and minor fixes were applied to helper modules to improve clarity and ensure clean compilation of assets.

## Useful links

- Dagster docs: https://docs.dagster.io/

