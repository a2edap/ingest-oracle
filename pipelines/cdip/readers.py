from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
import requests
from tsdat import DataReader


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
        # Get station number and data storage type
        station_number = input_key
        data_type = self.parameters.data_type

        if data_type == "historic":
            cdip_archive = (
                "https://thredds.cdip.ucsd.edu/thredds/fileServer/cdip/archive"
            )
            data_url = (
                f"{cdip_archive}/{station_number}p1/{station_number}p1_historic.nc"
            )
        elif data_type == "realtime":
            cdip_realtime = (
                "https://thredds.cdip.ucsd.edu/thredds/fileServer/cdip/realtime"
            )
            data_url = f"{cdip_realtime}/{station_number}p1_rt.nc"

        # Create filename to download file into
        fname = f"cdip.{station_number}.{data_type}.nc"

        print(f"Downloading file {data_url}...")
        r = requests.get(data_url)
        open(fname, "wb").write(r.content)

        print(f"Download complete.")
        ds = xr.open_dataset(fname)
        ds.attrs["cdip_title"] = ds.attrs["title"]  # reset in pipeline hook
        ds.attrs["fname"] = fname  # removed in pipeline hook

        return ds
