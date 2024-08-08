from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
from tsdat import DataReader
from datetime import datetime
from datetime import timedelta


class NOAATempReader(DataReader):

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomDataReader should take any additional arguments from the
        retriever configuration file, then those should be specified here.

        e.g.,:
        custom_parameter: float = 5.0

        """

    parameters: Parameters = Parameters()

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        f = open(input_key, "r")
        Time = []

        lineZero = f.readline()
        lineOne = f.readline()
        lineTwo = f.readline()

        lineThree = f.readline()
        locations = lineThree.split()
        Latitude = float(locations[0])
        Longitude = float(locations[1])
        Elevation = float(locations[2])

        lineFour = f.readline()
        times = lineFour.split()

        lineFive = f.readline()
        counts = lineFive.split()
        AvgTime = int(counts[0])

        lineSix = f.readline()
        lineSeven = f.readline()
        lineEight = f.readline()
        lineNine = f.readline()
        lineTen = f.readline()

        Height = []
        MeanUncorrectedRASSTemp = []
        MeanCorrectedRASSTemp = []
        MeanVeriticalWind = []
        NumRecMeanUnCorrRASS = []
        NumRecMeanCorrRASS = []
        NumRecMeanVW = []
        SNRMeanUnCorrRASS = []
        SNRMeanCorrRASS = []
        SNRMeanVW = []
        seenDollar = False

        for line in f:
            data = line.split()
            if data and data[0] != "$":
                if not seenDollar:
                    if Time:
                        currentTime = Time[-1] + timedelta(minutes=AvgTime)
                        Time.append(currentTime)
                    else:
                        currentTime = datetime(
                            int(times[0]) + 2000,
                            int(times[1]),
                            int(times[2]),
                            int(times[3]),
                            int(times[4]),
                            int(times[5]),
                        )
                        Time.append(currentTime)
                    Height.append(float(data[0]))
                    MeanUncorrectedRASSTemp.append(float(data[1]))
                    MeanCorrectedRASSTemp.append(float(data[2]))
                    MeanVeriticalWind.append(float(data[3]))
                    NumRecMeanUnCorrRASS.append(float(data[4]))
                    NumRecMeanCorrRASS.append(float(data[5]))
                    NumRecMeanVW.append(float(data[6]))
                    SNRMeanUnCorrRASS.append(float(data[7]))
                    SNRMeanCorrRASS.append(float(data[8]))
                    SNRMeanVW.append(float(data[9]))
            else:
                seenDollar = True

        data_vars = {
            "height": (["time"], Height),
            "mean_uncorrected_RASS_temperature": (["time"], MeanUncorrectedRASSTemp),
            "mean_corrected_RASS_temperature": (["time"], MeanCorrectedRASSTemp),
            "mean_vertical_wind": (["time"], MeanVeriticalWind),
            "number_of_records_mean_uncorrected_RASS_temperature": (
                ["time"],
                NumRecMeanUnCorrRASS,
            ),
            "number_of_records_mean_corrected_RASS_temperature": (
                ["time"],
                NumRecMeanCorrRASS,
            ),
            "number_of_records_mean_vertical_wind": (["time"], NumRecMeanVW),
            "SNR_mean_uncorrected_RASS_temperature": (["time"], SNRMeanUnCorrRASS),
            "SNR_mean_corrected_RASS_temperature": (["time"], SNRMeanCorrRASS),
            "SNR_mean_vertical_wind": (["time"], SNRMeanVW),
            "latitude": ([], Latitude, {}),
            "longitude": ([], Longitude, {}),
            "elevation": ([], Elevation, {}),
        }
        # define coordinates
        coords = {"time": (["time"], Time)}

        # create dataset
        ds = xr.Dataset(data_vars=data_vars, coords=coords)
        ds = ds.where(ds != 999999.0, -9999)
        return ds
