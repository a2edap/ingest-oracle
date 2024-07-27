import xarray as xr

from tsdat import IngestPipeline
import cftime
import numpy as np
from datetime import datetime


class PilotRadiosonde(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        value_to_drop = cftime.DatetimeGregorian(
            -29, 8, 17, 0, 0, 0, 0, has_year_zero=False
        )
        valid_time_condition = dataset.time != value_to_drop
        ds_filtered = dataset.where(valid_time_condition, drop=True)

        def convert_to_datetime(t):
            if isinstance(t, cftime.datetime):
                return np.datetime64(
                    datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
                )
            else:
                return t

        ds_filtered["time"] = np.array(
            [convert_to_datetime(t) for t in ds_filtered["time"].values]
        )

        return ds_filtered

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        pass
