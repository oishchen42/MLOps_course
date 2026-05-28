from pathlib import Path
import dagster as dg
from .defs import assets
import pandas as pd


#TODO: Implement a custom IOManager to handle CSV read/write operations for assets. This will allow us to persist asset outputs as CSV files and load them when needed, enabling better data management and traceability across asset executions.
# class LocalCSVIOManager(dg.IOManager):
#     def handle_output(self, context, obj):
#         # --- EXPLORER AND DEBUG LOGGING ---
#         context.log.info(f"Handling output for asset: {context.asset_key}")
#         context.log.info(f"Output object type: {type(obj)}")
#         context.log.info(f"Output object preview:\n{str(obj)[:500]}")  # Log the first 500 characters of the output

#     def load_input(self, context):
#         """Loads the CSV when a downstream asset requires it."""
#         file_name = f"{context.asset_key.path[-1]}.csv"
#         return pd.read_csv(file_name)

all_assets = dg.load_assets_from_modules([assets])

defs = dg.Definitions(
    assets=all_assets,
    # resources={
    #     "io_manager": LocalCSVIOManager()
    # }
)