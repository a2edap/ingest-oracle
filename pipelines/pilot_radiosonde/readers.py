from datetime import datetime
from typing import Dict, Union

import numpy as np
import xarray as xr

from tsdat import DataReader


class pilot_radiosonde(DataReader):
    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        ds = xr.load_dataset(input_key)
        # for var_name in ds.variables:
        #     if np.issubdtype(
        #         ds[var_name].dtype, np.number
        #     ):  # Check if the variable is numeric
        #         ds[var_name] = ds[var_name].where(~np.isnan(ds[var_name]), -9999)

        return ds
