from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
from tsdat import DataReader
from datetime import datetime
from datetime import timedelta


# DEVELOPER: Implement or remove the CustomDataReader. If implementing it, please
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

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

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
        QualityC = []
        RadialVelocityBeam1 = []
        RadialVelocityBeam2 = []
        RadialVelocityBeam3 = []
        MeanObsBeam1 = []
        MeanObsBeam2 = []
        MeanObsBeam3 = []
        MeanSNRBeam1 = []
        MeanSNRBeam2 = []
        MeanSNRBeam3 = []
        QualityRVBeam1 = []
        QualityRVBeam2 = []
        QualityRVBeam3 = []
        seenDollar = False

        for line in f:
            data = line.split()
            if data[0] != "$":
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
                    WindSpeed.append(float(data[1]))
                    WindDirection.append(float(data[2]))
                    QualityC.append(int(data[3]))
                    RadialVelocityBeam1.append(float(data[4]))
                    RadialVelocityBeam2.append(float(data[5]))
                    RadialVelocityBeam3.append(float(data[6]))
                    MeanObsBeam1.append(int(data[7]))
                    MeanObsBeam2.append(int(data[8]))
                    MeanObsBeam3.append(int(data[9]))
                    MeanSNRBeam1.append(int(data[10]))
                    MeanSNRBeam2.append(int(data[11]))
                    MeanSNRBeam3.append(int(data[12]))
                    QualityRVBeam1.append(float(data[13]))
                    QualityRVBeam2.append(float(data[14]))
                    QualityRVBeam3.append(float(data[15]))

            else:
                seenDollar = True

        data_vars = {
            "height": (["time"], Height),
            "wind_speed": (["time"], WindSpeed),
            "wind_direction": (["time"], WindDirection),
            "QC_wind": (["time"], QualityC),
            "radial_velocity_beam_1": (["time"], RadialVelocityBeam1),
            "radial_velocity_beam_2": (["time"], RadialVelocityBeam2),
            "radial_velocity_beam_3": (["time"], RadialVelocityBeam3),
            "number_of_records_in_mean_beam_1": (["time"], MeanObsBeam1),
            "number_of_records_in_mean_beam_2": (["time"], MeanObsBeam2),
            "number_of_records_in_mean_beam_3": (["time"], MeanObsBeam3),
            "SNR_beam_1": (["time"], MeanSNRBeam1),
            "SNR_beam_2": (["time"], MeanSNRBeam2),
            "SNR_beam_3": (["time"], MeanSNRBeam3),
            "qc_radial_velocity_beam_1": (["time"], QualityRVBeam1),
            "qc_radial_velocity_beam_2": (["time"], QualityRVBeam2),
            "qc_radial_velocity_beam_3": (["time"], QualityRVBeam3),
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

        for var_name in ds.data_vars:
            ds[var_name] = ds[var_name].where(ds[var_name] != 999999.0, -9999)

        return ds
