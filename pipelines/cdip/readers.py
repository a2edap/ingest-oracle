from typing import Dict, Union
from pydantic import BaseModel, Extra
import numpy as np
import xarray as xr

from tsdat import DataReader
from mhkit.wave.io.cdip import request_netCDF


class CDIPDataRequest(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that pulls netcdf data from CDIP archives

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """Extra parameters that can be set via the retrieval configuration file."""

        data_type: str = "realtime"

    parameters: Parameters = Parameters()

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        def unique_time(ds, time_var):
            # Remove repeated timestamps if they exist
            _, index = np.unique(ds[time_var], return_index=True)

            if len(index) == len(ds[time_var]):
                return ds
            else:
                return ds.isel({time_var: index})

        def clean_netcdf(nc):
            ds = xr.open_dataset(xr.backends.NetCDF4DataStore(nc))

            excess_dims = ["sourceCount", "metaBoundsCount"]
            ds = ds.drop_dims(excess_dims)

            # Check for duplicate timestamps
            # map all the time coordinates to a single time (waveTime) - skip for later
            time_vars = [v for v in ds.coords if "time" in v.lower()]
            time_vars.remove("waveTime")
            for tm in time_vars:
                ds = unique_time(ds, tm)

            return ds

        # input_key is the station id #
        nc = request_netCDF(input_key, data_type=self.parameters.data_type)
        ds = clean_netcdf(nc)

        return ds
