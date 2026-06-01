# Production Project: MLOps and Dagster

This repository collects the LEVEL3 workshop artifacts: ML notebooks, datasets, analysis plots, and a Dagster pipeline for the bike rentals use case.

## Key materials

- Course overview and handouts: [mlops/README.md](mlops/README.md)
- Notebooks: [notebook/week1_titanic1.ipynb](notebook/week1_titanic1.ipynb), [notebook/week1_titanic2.ipynb](notebook/week1_titanic2.ipynb), [notebook/week2_bikes1.ipynb](notebook/week2_bikes1.ipynb)
- Exported figures: [diagrams/simple_baseline.png](diagrams/simple_baseline.png)
- Titanic template data: [templates/titanic.csv](templates/titanic.csv)
- Dagster project: [bikes_dagster/README.md](bikes_dagster/README.md)

## Data sources

- Titanic dataset: [mlops/week-1/data/titanic.csv](mlops/week-1/data/titanic.csv)
- Bike rentals datasets: [mlops/week-2/data/direct_pickup_bike_rentals.csv](mlops/week-2/data/direct_pickup_bike_rentals.csv), [mlops/week-2/data/registered_bike_rentals.csv](mlops/week-2/data/registered_bike_rentals.csv), [mlops/week-2/data/weather.csv](mlops/week-2/data/weather.csv), [mlops/week-2/data/holidays.csv](mlops/week-2/data/holidays.csv)

## Dagster pipeline (bike rentals)

The Dagster project in [bikes_dagster/README.md](bikes_dagster/README.md) builds assets from the week-2 bike rental CSVs and produces a feature-engineered dataset. Asset definitions live in [bikes_dagster/src/bikes/defs/assets.py](bikes_dagster/src/bikes/defs/assets.py).

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

