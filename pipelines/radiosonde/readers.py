from typing import Dict, Union
from pydantic import BaseModel, Extra


from tsdat import DataReader

import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class RadiosondeReader(DataReader):
    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomDataReader should take any additional arguments from the
        retriever configuration file, then those should be specified here.

        e.g.,:
        custom_parameter: float = 5.0

        """

    missing_values = ["MM", 9999, 999, 99]

    parameters: Parameters = Parameters()

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        f = open(input_key, "r")

        lineZero = f.readline()
        pressure_level_data_source = lineZero[37:45].strip()
        non_pressure_level_data_source = lineZero[46:54].strip()
        Latitude = float(lineZero[55:62]) / 1000.0
        Longitude = float(lineZero[63:71]) / 1000.0
        Year = int(lineZero[13:17])
        Month = int(lineZero[18:20])
        Day = int(lineZero[21:23])
        Hour = int(lineZero[24:26])
        RelTime = lineZero[27:31]

        hour = int(RelTime[:2])
        minute = int(RelTime[-2:])

        start_datetime = datetime(Year, Month, Day, hour, minute)

        # var_lists
        major_level_type = []
        minor_level_type = []
        ETIME = []
        pressure = []
        pressure_processing_flag = []
        geopotential_height = []
        geopotential_height_processing_flag = []
        temperature = []
        temperature_processing_flag = []
        relative_humidity = []
        dewpoint_depression = []
        wind_direction = []
        wind_speed = []

        for line in f:
            major_level_type.append(int(line[0]))
            minor_level_type.append(int(line[1:2]))
            ETIME.append(int(line[3:8]))
            pressure.append(int(line[9:15]) / 100)
            pressure_processing_flag.append(line[15:16])
            geopotential_height.append(int(line[16:21]))
            geopotential_height_processing_flag.append(line[21:22])
            temperature.append(int(line[22:27]))
            temperature_processing_flag.append(line[27:28])
            relative_humidity.append(int(line[28:33]))
            dewpoint_depression.append(int(line[34:39]))
            wind_direction.append(int(line[40:45]))
            wind_speed.append(int(line[46:51]))

        time = []
        last_datetime = start_datetime
        use_last_datetime = False
        for etime in ETIME:
            total_seconds = int(etime)
            minutes = total_seconds // 100
            seconds = total_seconds % 100
            delta = timedelta(minutes=minutes, seconds=seconds)

            if total_seconds == 100:
                use_last_datetime = True

            if use_last_datetime:
                new_datetime = last_datetime + delta
            else:
                new_datetime = start_datetime + delta

            time.append(np.datetime64(new_datetime))
            last_datetime = new_datetime

        data_vars = {
            "major_level_type": (["time"], major_level_type),
            "minor_level_type": (["time"], minor_level_type),
            "pressure": (["time"], pressure),
            "pressure_processing_flag": (["time"], pressure_processing_flag),
            "geopotential_height": (
                ["time"],
                geopotential_height,
            ),
            "geopotential_height_processing_flag": (
                ["time"],
                geopotential_height_processing_flag,
            ),
            "temperature": (["time"], temperature),
            "temperature_processing_flag": (["time"], temperature_processing_flag),
            "relative_humidity": (["time"], relative_humidity),
            "dewpoint_depression": (["time"], dewpoint_depression),
            "wind_direction": (["time"], wind_direction),
            "wind_speed": (["time"], wind_speed),
            "pressure_level_data_source": ([], pressure_level_data_source, {}),
            "non_pressure_level_data_source": ([], non_pressure_level_data_source, {}),
            "latitude": ([], Latitude, {}),
            "longitude": ([], Longitude, {}),
        }

        coords = {"time": (["time"], time)}

        ds = xr.Dataset(data_vars=data_vars, coords=coords)

        return ds
