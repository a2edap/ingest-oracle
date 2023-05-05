from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
from tsdat import DataReader


class FetchHFRadarData(DataReader):
    """---------------------------------------------------------------------------------
    Fetches high-frequency radar netcdf4 data from the UCSD THREDDS database.
    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomDataReader should take any additional arguments from the
        retriever configuration file, then those should be specified here.
        """

        start_date: str = "2012-01-01"
        end_date: str = "2012-02-01"
        resolution: str = "6km"  # 1km, 2km, or 6km

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        """----------------------------------------------------------------------------
        1 km data, 1 month at a time
        https://hfrnet-tds.ucsd.edu/thredds/ncss/HFR/USWC/1km/hourly/RTV/HFRADAR_US_West_Coast_1km_Resolution_Hourly_RTV_best.ncd?var=u&var=v&north=39.0&west=-125.0&east=-117.0&south=32.5&disableProjSubset=on&horizStride=1&time_start=2012-01-01T00%3A00%3A00Z&time_end=2012-02-01T00%3A00%3A00Z&timeStride=1&addLatLon=true&accept=netcdf4

        2 km data, 1 month at a time
        https://hfrnet-tds.ucsd.edu/thredds/ncss/HFR/USWC/2km/hourly/RTV/HFRADAR_US_West_Coast_2km_Resolution_Hourly_RTV_best.ncd?var=u&var=v&north=39.0&west=-125.0&east=-117.0&south=32.5&disableProjSubset=on&horizStride=1&time_start=2012-01-01T00%3A00%3A00Z&time_end=2012-02-01T18%3A00%3A00Z&timeStride=1&addLatLon=true&accept=netcdf4

        6 km data, 1 month at a time
        https://hfrnet-tds.ucsd.edu/thredds/ncss/HFR/USWC/6km/hourly/RTV/HFRADAR_US_West_Coast_6km_Resolution_Hourly_RTV_best.ncd?var=u&var=v&north=39.0&west=-125.0&east=-117.0&south=32.5&disableProjSubset=on&horizStride=1&time_start=2012-01-01T00%3A00%3A00Z&time_end=2012-02-01T00%3A00%3A00Z&timeStride=1&addLatLon=true&accept=netcdf4
        ----------------------------------------------------------------------------"""

        res = self.parameters.resolution
        start = self.parameters.start_date
        end = self.parameters.end_date

        website = f"https://hfrnet-tds.ucsd.edu/thredds/ncss/HFR/USWC/{res}/hourly/RTV/HFRADAR_US_West_Coast_{res}_Resolution_Hourly_RTV_best.ncd?var=u&var=v&north=39.0&west=-125.0&east=-117.0&south=32.5&disableProjSubset=on&horizStride=1&time_start={start}T00%3A00%3A00Z&time_end={end}T18%3A00%3A00Z&timeStride=1&addLatLon=true&accept=netcdf4"

        return xr.Dataset()
