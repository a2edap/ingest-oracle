from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
from tsdat import DataReader
from datetime import datetime
from datetime import timedelta


class CustomDataReader(DataReader):
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
        stationNames = lineOne.split()
        StationsID = stationNames[0]

        lineTwo = f.readline()
        dataInfo = lineTwo.split()
        DataType = dataInfo[0]
        RevisionNum = float(dataInfo[2])

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
        WindSpeed = []
        WindDirection = []
        RadialVelocityBeam1 = []
        RadialVelocityBeam2 = []
        RadialVelocityBeam3 = []
        MeanObsBeam1 = []
        MeanObsBeam2 = []
        MeanObsBeam3 = []
        MeanSNRBeam1 = []
        MeanSNRBeam2 = []
        MeanSNRBeam3 = []
        blockCounter = 0
        lines_to_skip = 0

        for line in f:
            if lines_to_skip > 0:
                lines_to_skip -= 1
                continue

            data = line.split()
            if blockCounter == 0 and data[0] != "$":
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
                WindSpeed.append(float(data[1]))
                WindDirection.append(float(data[2]))
                RadialVelocityBeam1.append(float(data[3]))
                RadialVelocityBeam2.append(float(data[4]))
                RadialVelocityBeam3.append(float(data[5]))
                MeanObsBeam1.append(int(data[6]))
                MeanObsBeam2.append(int(data[7]))
                MeanObsBeam3.append(int(data[8]))
                MeanSNRBeam1.append(int(data[9]))
                MeanSNRBeam2.append(int(data[10]))
                MeanSNRBeam3.append(int(data[11]))

            elif blockCounter == 2 and data[0] != "$":
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
                WindSpeed.append(float(data[1]))
                WindDirection.append(float(data[2]))
                RadialVelocityBeam1.append(float(data[3]))
                RadialVelocityBeam2.append(float(data[4]))
                RadialVelocityBeam3.append(float(data[5]))
                MeanObsBeam1.append(int(data[6]))
                MeanObsBeam2.append(int(data[7]))
                MeanObsBeam3.append(int(data[8]))
                MeanSNRBeam1.append(int(data[9]))
                MeanSNRBeam2.append(int(data[10]))
                MeanSNRBeam3.append(int(data[11]))

            elif data[0] == "$":
                blockCounter += 1
                lines_to_skip = 36 if blockCounter == 1 else 11
                if blockCounter == 3:
                    break

        data_vars = {
            "height": (["time"], Height),
            "wind_speed": (["time"], WindSpeed),
            "wind_direction": (["time"], WindDirection),
            "radial_velocity_beam_1": (["time"], RadialVelocityBeam1),
            "radial_velocity_beam_2": (["time"], RadialVelocityBeam2),
            "radial_velocity_beam_3": (["time"], RadialVelocityBeam3),
            "number_of_records_in_mean_beam_1": (["time"], MeanObsBeam1),
            "number_of_records_in_mean_beam_2": (["time"], MeanObsBeam2),
            "number_of_records_in_mean_beam_3": (["time"], MeanObsBeam3),
            "SNR_beam_1": (["time"], MeanSNRBeam1),
            "SNR_beam_2": (["time"], MeanSNRBeam2),
            "SNR_beam_3": (["time"], MeanSNRBeam3),
            "latitude": ([], Latitude, {}),
            "longitude": ([], Longitude, {}),
            "elevation": ([], Elevation),
        }
        # define coordinates
        coords = {"time": (["time"], Time)}

        attrs = {
            "station_ID": StationsID,
            "data_type": DataType,
            "revision_number": RevisionNum,
        }

        # create dataset
        ds = xr.Dataset(data_vars=data_vars, coords=coords, attrs=attrs)

        return ds
