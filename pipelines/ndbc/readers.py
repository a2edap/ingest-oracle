from typing import Dict, Union
from pydantic import BaseModel, Extra


from tsdat import DataReader

import xarray as xr
import pandas as pd
import numpy as np


# DEVELOPER: Implement or remove the CustomDataReader. If implement ing it, please
# rename it to appropriately reflect the type of data it is reading.
class CustomDataReader(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomDataReader should take any additional arguments from the
        retriever configuration file, then those should be specified here.

        e.g.,:
        custom_parameter: float = 5.0

        """

    missing_values = ["MM", 9999, 999, 99]

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        ## code is the read function from mhkit/wave/io/ndbc.py in the mhkit package
        ## with additional data manipulation to make return one dataarray.
        missing_values = ["MM", 9999, 999, 99]
        assert isinstance(input_key, str), "input_key must be of type str"
        assert isinstance(missing_values, list), "missing_values must be of type list"

        # Open file and get header rows
        f = open(input_key, "r")
        header = f.readline().rstrip().split()  # read potential headers
        units = f.readline().rstrip().split()  # read potential units
        f.close()

        # If first line is commented, remove comment sign #
        if header[0].startswith("#"):
            header[0] = header[0][1:]
            header_commented = True
        else:
            header_commented = False

        # If second line is commented, indicate that units exist
        if units[0].startswith("#"):
            units_exist = True
        else:
            units_exist = False

        # Check if the time stamp contains minutes, and create list of column names
        # to parse for date
        if header[4] == "mm":
            parse_vals = header[0:5]
            date_format = "%Y %m %d %H %M"
            units = units[5:]  # remove date columns from units
        else:
            parse_vals = header[0:4]
            date_format = "%Y %m %d %H"
            units = units[4:]  # remove date columns from units

        # If first line is commented, manually feed in column names
        if header_commented:
            data = pd.read_csv(
                input_key,
                sep="\s+",
                header=None,
                names=header,
                comment="#",
                parse_dates=[parse_vals],
            )
        # If first line is not commented, then the first row can be used as header
        else:
            data = pd.read_csv(
                input_key, sep="\s+", header=0, comment="#", parse_dates=[parse_vals]
            )

        # Convert index to datetime
        date_column = "_".join(parse_vals)
        data["Time"] = pd.to_datetime(data[date_column], format=date_format)
        data.index = data["Time"].values
        # Remove date columns
        del data[date_column]
        del data["Time"]

        # If there was a row of units, convert to dictionary
        if units_exist:
            metadata = {column: unit for column, unit in zip(data.columns, units)}
        else:
            metadata = None

        # Convert columns to numeric data if possible, otherwise leave as string
        for column in data:
            data[column] = pd.to_numeric(data[column], errors="ignore")

        # Convert column names to float if possible (handles frequency headers)
        # if there is non-numeric name, just leave all as strings.
        try:
            data.columns = [float(column) for column in data.columns]
        except:
            data.columns = data.columns

        # Replace indicated missing values with nan
        data.replace(missing_values, np.nan, inplace=True)

        # convert data frame to xarray
        df = data.to_xarray()
        # added meta data as units
        if metadata:
            for key in metadata:
                df[key].attrs = {"units": metadata[key]}
        # rename index
        df = df.rename({"index": "time"})

        # return data, metadata
        return df
