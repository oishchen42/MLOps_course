import dagster as dg
import pandas as pd
import supply as sp
import lakefs

@dg.asset(
    group_name="initial_load",
    compute_kind="lakeFS"
)
def lakefs_raw_ingestion(context: dg.AssetExecutionContext) -> dict:
    repo = lakefs.repository("bike-rentals")
    branch_name = "dev"
    
    try:
        working_branch = repo.branch(branch_name).create(source_reference="main")
    except Exception:
        working_branch = repo.branch(branch_name)
    
    raw_direct = pd.read_csv(sp.PATH_DIRECT_PICKUP_BIKE)
    raw_registered = pd.read_csv(sp.PATH_REGISTERED_BIKE)
    raw_holidays = pd.read_csv(sp.PATH_HOLIDAYS)
    raw_weather = pd.read_csv(sp.PATH_WEATHER)
    
    direct_path = "data/raw/direct_rentals.csv"
    registered_path = "data/raw/registered_rentals.csv"
    holidays_path = "data/raw/holidays.csv"
    weather_path = "data/raw/weather.csv"
    
    with working_branch.object(direct_path).writer() as f:
        raw_direct.to_csv(f, index=False)
    with working_branch.object(registered_path).writer() as f:
        raw_registered.to_csv(f, index=False)
    with working_branch.object(holidays_path).writer() as f:
        raw_holidays.to_csv(f, index=False)
    with working_branch.object(weather_path).writer() as f:
        raw_weather.to_csv(f, index=False)

    working_branch.commit(message=f"Raw data ingested for Dagster run {context.run_id[:8]}")
    
    return {
        "direct_uri": f"lakefs://bike-rentals/{branch_name}/{direct_path}",
        "registered_uri": f"lakefs://bike-rentals/{branch_name}/{registered_path}",
        "holidays_uri": f"lakefs://bike-rentals/{branch_name}/{holidays_path}",
        "weather_uri": f"lakefs://bike-rentals/{branch_name}/{weather_path}"
    }