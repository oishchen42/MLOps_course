import os
from pathlib import Path
import dagster as dg
import pandas as pd

# 1. IMPORT YOUR MODULES HERE
# This tells Python where to find first_stage, bikes_merge, etc.
from .defs import first_stage, bikes_merge, united_bikes_holidays, united_all

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

# 2. ASSEMBLE THE ASSETS
# Python now recognizes these names because they were imported above
all_assets = dg.load_assets_from_modules([
    first_stage,
    bikes_merge,
    united_bikes_holidays,
    united_all
])

defs = dg.Definitions(
    assets=all_assets,
    resources={
        "csv_export": LocalCSVIOManager(base_dir="data_warehouse")
    }
)