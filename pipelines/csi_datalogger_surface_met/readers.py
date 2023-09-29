from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
import pandas as pd 
from tsdat import DataReader
from datetime import datetime



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
        # DEVELOPER: Implement the read method. This takes an input_key which is the path
        # to the file being run. It should open the file and return either a single
        # Dataset object, or a mapping of strings to Datasets.
        data = pd.read_csv(input_key, header=None)
        location_id = input_key[43:46]
        Hour = input_key[65:67]
        #print(Hour)
        metadata = open("/share/home/ocoleman/meta_met/" + location_id + ".txt", "r")

        #read the first line and save the first time stamp 
        time_str = metadata.readline()
        times = time_str.split(" UTC")
        str_time = times[0]
        dt = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        #make empty variables to hold data 
        meta = {}
        features = []

        for x in metadata:
            #if the line is the start of a year 
            if x[0] == "2":
                #add the current data to the dictionary 
                meta[dt] = features
                #save the new time stamp over the old one and clear the features variable 
                times = x.split(" UTC")
                str_time1 = times[0]
                dt = datetime.strptime(str_time1, "%Y-%m-%d %H:%M:%S")
                features = []
            else:
                #append to list of fetures 
                features.append(x.strip())
        #save the last set of features to the dictionary 
        meta[dt] = features  

        #look at the first date in the dataset to figure out what meta data to use 
        first_time = data.iloc[0,1:4]
        year = str(round(first_time.iloc[0]))
        day = str(round(first_time.iloc[1]))
        hourMin = str(round(first_time.iloc[2]))
        if len(hourMin) >= 3:
            mini = hourMin[-2:]
        else:
            mini = hourMin
        #print(mini)

        #turn date into time stamp 
        timestamp = datetime.strptime(datetime.strptime(year + "-" + day + " " + Hour + " " + mini, "%Y-%j %H %M").strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        #loop trew dictionary to get list 
        colNames = []
        foundCol = False
        for entry in meta:
            if foundCol == False:
                if entry < timestamp:
                    colNames = meta.get(entry)
                    foundCol = True

        #add column names to the data
        data.columns = colNames

        #make a list of all the data convereted to timestamps 
        time_list = []
        for x in range (0, data.shape[0]):
            first_time = data.iloc[x,1:4]
            year = str(round(first_time.iloc[0]))
            day = str(round(first_time.iloc[1]))    
            hourMin = str(round(first_time.iloc[2]))
            if len(hourMin) >= 3:
                mini = hourMin[-2:]
            else:
                mini = hourMin
            #print(mini)
            timestamp = datetime.strptime(datetime.strptime(year + "-" + day + " " + Hour + " " + mini, "%Y-%j %H %M").strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
            time_list.append(timestamp)
        #print (time_list)

        #add the time stamps to the data and make it the new index 
        data = data.assign(time=time_list)
        data.index = data["time"].values
        del data["time"]
        # convert data frame to xarray
        df = data.to_xarray()
        # rename index
        df = df.rename({"index": "time"})
        return df
