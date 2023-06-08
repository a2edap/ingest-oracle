import pandas as pd
from utils.registry import PipelineRegistry


buoy_list = pd.read_csv("pipelines/cdip/cdip_buoy_list.txt", header=0)

dispatcher = PipelineRegistry()
dispatcher.dispatch(buoy_list, clump=False, multidispatch=True)
