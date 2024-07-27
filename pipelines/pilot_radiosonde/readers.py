from datetime import datetime
from typing import Dict, Union

import numpy as np
import xarray as xr

from tsdat import DataReader


class pilot_radiosonde(DataReader):
    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        ds = xr.load_dataset(input_key).swap_dims({"altitude": "time"}).reset_coords()

        return ds
