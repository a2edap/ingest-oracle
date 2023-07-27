from typing import Dict, Union
from pydantic import BaseModel, Extra
import numpy as np
import xarray as xr
import errno
import os
import signal
import functools

from tsdat import DataReader


## Class and decorator to handle corrupted data variables
class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


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
        def request_netCDF(station_number, data_type):
            if data_type == "historic":
                cdip_archive = "http://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/archive"
                data_url = (
                    f"{cdip_archive}/{station_number}p1/{station_number}p1_historic.nc"
                )
            elif data_type == "realtime":
                cdip_realtime = (
                    "http://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime"
                )
                data_url = f"{cdip_realtime}/{station_number}p1_rt.nc"
            return data_url

        def unique_time(ds, time_var):
            # Remove repeated timestamps if they exist
            _, index = np.unique(ds[time_var], return_index=True)

            if len(index) == len(ds[time_var]):
                return ds
            else:
                return ds.isel({time_var: index})

        def clean_netcdf(ds):
            # Check for duplicate timestamps
            # map all the time coordinates to a single time (waveTime) - skip for later
            time_vars = [v for v in ds.coords if "time" in v.lower()]
            time_vars.remove("waveTime")
            # Drop unecessary coordinates to speed up pipeline
            time_vars_to_keep = ["sstTime", "gpsTime", "dwrTime", "waveTime"]

            if "dwrTime" not in time_vars:
                ds["dwrTime"] = ds["waveTime"].copy()

            for tm in time_vars:
                if tm not in time_vars_to_keep:
                    ds = ds.drop_dims(tm)
                else:
                    ds = unique_time(ds, tm)

            return ds

        @timeout(10)
        def check_corrupted_vars(ds, var):
            ds[var].isnull()

        # input_key is the station id #
        url = request_netCDF(input_key, data_type=self.parameters.data_type)
        ds = xr.open_dataset(url)
        ds = clean_netcdf(ds)
        ds.attrs["cdip_title"] = ds.attrs["title"]  # reset in pipeline hook

        for var in ds.data_vars:
            try:
                check_corrupted_vars(ds, var)
            except TimeoutError:
                ds = ds.drop_vars(var)

        return ds
