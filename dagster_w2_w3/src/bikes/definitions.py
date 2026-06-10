import os
from pathlib import Path
import dagster as dg
import pandas as pd

from .defs import first_stage, bikes_merge, united_bikes_holidays, united_all, machine_data_prep, models_linear_prep, models_linear_reg, models_xgb_reg, models_xgboost

class LocalCSVIOManager(dg.ConfigurableIOManager):
    base_dir: str

    def _get_path(self, context) -> Path:
        file_name = f"{context.asset_key.path[-1]}.csv"
        return Path(self.base_dir) / file_name

    def handle_output(self, context, obj: pd.DataFrame):
        file_path = self._get_path(context)
        
        # os is now imported at the top, so this will work
        os.makedirs(file_path.parent, exist_ok=True)
        
        obj.to_csv(file_path, index=False)
        context.log.info(f"Successfully saved CSV to: {file_path}")

    def load_input(self, context) -> pd.DataFrame:
        file_path = self._get_path(context)
        context.log.info(f"Loading CSV from: {file_path}")
        return pd.read_csv(file_path)


all_assets = dg.load_assets_from_modules([
    first_stage,
    bikes_merge,
    united_bikes_holidays,
    united_all,
    machine_data_prep,
    models_linear_prep,
    models_linear_reg,
    models_xgb_reg,
    models_xgboost
])

defs = dg.Definitions(
    assets=all_assets,
    resources={
        "csv_export": LocalCSVIOManager(base_dir="data_warehouse")
    }
)