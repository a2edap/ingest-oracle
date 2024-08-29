from typing import Dict, Union
import xarray as xr
import cftime
import pandas as pd
from tsdat import DataReader


class pilot_radiosonde(DataReader):
    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        ds = xr.load_dataset(input_key).swap_dims({"altitude": "time"}).reset_coords()

        value_to_drop = cftime.DatetimeGregorian(
            -29, 8, 17, 0, 0, 0, 0, has_year_zero=False
        )
        valid_time_condition = ds.time != value_to_drop
        ds_filtered = ds.where(valid_time_condition, drop=True)

        if "time" in ds_filtered.coords:
            time_data = ds_filtered["time"].values

            if isinstance(time_data[0], cftime.DatetimeGregorian):
                time_data_str = time_data.astype(str)

                time_data = pd.to_datetime(
                    time_data_str, format="mixed", errors="coerce"
                )

                ds_filtered["time"] = ("time", time_data)

        return ds_filtered
