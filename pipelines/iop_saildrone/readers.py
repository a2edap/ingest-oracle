from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
from tsdat import DataReader


class SaildroneReader(DataReader):
    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        ds = xr.open_dataset(input_key, group="atmospheric")
        return ds
