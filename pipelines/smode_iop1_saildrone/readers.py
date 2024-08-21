from datetime import datetime
from typing import Dict, Union

import numpy as np
import xarray as xr

from tsdat import DataReader


class pilot_saildrone(DataReader):
    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        ds = xr.load_dataset(input_key)

        # Rename dimension and adjust 'time' coordinate
        ds = ds.rename({"obs": "time"})
        time_only = ds["time"].isel(trajectory=0).drop_vars("trajectory")
        ds = ds.drop_vars("time").assign_coords(time=("time", time_only.data))

        # Convert 'latitude' and 'longitude' from coordinates to data variables
        ds = ds.reset_coords(["latitude", "longitude"], drop=False)

        ds = ds.transpose()

        return ds
