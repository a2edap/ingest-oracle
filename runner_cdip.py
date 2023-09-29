import pandas as pd
import gc
from utils.registry import PipelineRegistry


buoy_list = pd.read_csv(
    "pipelines/cdip/cdip_buoy_list.txt", header=None, dtype=str
).T.values[0]

for buoy in buoy_list:
    try:
        dispatcher = PipelineRegistry()
        dispatcher.dispatch([str(buoy)], clump=False, multidispatch=True)
    except:
        del dispatcher
    print(buoy)

    gc.collect()
