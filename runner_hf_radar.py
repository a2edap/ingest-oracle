import numpy as np
from utils.registry import PipelineRegistry

# List of months
start_dates = np.arange(np.datetime64("2012-01"), np.datetime64("2023-06")).astype(str)

dispatcher = PipelineRegistry()
dispatcher.dispatch(start_dates, clump=False, multidispatch=True)
